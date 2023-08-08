use pyo3::prelude::*;
use std::collections::HashMap;
use pyo3::types::PyDict;
use std::time;

#[pyclass(module = "nova_python", frozen)]
#[derive(PartialEq)]
#[derive(Clone)]
enum Models {
    #[pyo3(name = "GPT3")]
    Gpt3,
    #[pyo3(name = "GPT4")]
    Gpt4,
    #[pyo3(name = "MODERATION_LATEST")]
    ModerationLatest,
    #[pyo3(name = "MODERATION_STABLE")]
    ModerationStable,
}

#[pyclass(module = "nova_python", frozen)]
#[derive(PartialEq)]
#[derive(Clone)]
enum Endpoints {
    #[pyo3(name = "CHAT_COMPLETION")]
    ChatCompletion,
    #[pyo3(name = "MODERATION")]
    Moderation,
}

#[pyclass(module = "nova_python", frozen)]
struct NovaClient {
    #[pyo3(get)]
    api_key: String,
    url: String
}

#[pymethods]
impl NovaClient {
    #[new]
    fn new(api_key: String) -> PyResult<Self> {
        let api_key = api_key.trim().to_string();
        
        if !key_is_valid(&api_key) {
            return Err(NovaClient::get_invalid_key_error());
        }

        Ok(NovaClient {
            api_key,
            url: String::from("https://api.nova-oss.com/v1/")
        })
    }

    fn make_request(&self, endpoint: Endpoints, model: Models, data: Vec<Py<PyDict>>) -> PyResult<String> {
        if !model_is_compatible(&endpoint, &model) {
            return Err(NovaClient::get_endpoint_not_compatible_error());
        }

        let request_url = self.get_request_url(&endpoint).unwrap();
        let request_body = self.get_request_body(&endpoint, &model, data).unwrap();

        let rt = tokio::runtime::Runtime::new().unwrap();
        
        let response: Result<String, reqwest::Error> = rt.block_on(async {
            let client = reqwest::Client::builder()
                .timeout(time::Duration::from_secs(10))
                .user_agent("Mozilla/5.0")
                .build()
                .unwrap();

            let ai_response = client.post(&request_url)
                .header("Authorization", format!("Bearer {}", self.api_key))
                .header("Content-Type", "application/json")
                .body(request_body)
                .send()
                .await?;
            
            let text = ai_response.text().await?;
            Ok(text)
        });

        match response {
            Ok(response) => Ok(response),
            Err(response) => Err(pyo3::exceptions::PyRuntimeError::new_err(response.to_string()))
        }
    }

}

impl NovaClient {
    fn get_request_url(&self, endpoint: &Endpoints) -> PyResult<String> {
        match endpoint {
            Endpoints::ChatCompletion => Ok(format!("{}chat/completions", self.url)),
            Endpoints::Moderation => Ok(format!("{}moderations", self.url)),
            _ => Err(NovaClient::get_invalid_endpoint_error())
        }
    }

    fn get_request_body(&self, endpoint: &Endpoints, model: &Models, data: Vec<Py<PyDict>>) -> PyResult<String> {
        let request_data = Python::with_gil(|py| {
            let mut request_data = Vec::new();

            for dict in data {
                let dict = dict.as_ref(py).extract::<HashMap<String, String>>().unwrap_or(HashMap::new());
                request_data.push(dict);
            }

            request_data
        });

        let mut request_body = String::from("{");

        let model = match model {
            Models::Gpt3 => "gpt-3.5-turbo",
            Models::Gpt4 => "gpt-4",
            Models::ModerationLatest => "text-moderation-latest",
            Models::ModerationStable => "text-moderation-stable",
            _ => return Err(NovaClient::get_invalid_model_error())
        };
        request_body.push_str(&format!("\"model\":\"{}\"", model));

        if endpoint == &Endpoints::ChatCompletion {
            request_body.push_str(",\"messages\":[");

            for map in request_data {

                request_body.push_str("{");
                for (key, value) in map {
                    request_body.push_str(&format!("\"{}\":\"{}\",", key, value));
                }
                
                if request_body.ends_with(",") {
                    request_body.pop();
                }

                request_body.push_str("},");
            }

            if request_body.ends_with(",") {
                request_body.pop();
            }
            
            request_body.push_str("]");

        } 
        
        else if endpoint == &Endpoints::Moderation {
            request_body.push_str(",\"input\":");

            let input = format!("\"{}\"", request_data.get(0).unwrap().get("input").unwrap());
            request_body.push_str(&input);
        }

        else {
            return Err(NovaClient::get_invalid_endpoint_error());
        }

        request_body.push_str("}");
        Ok(request_body)
    }

    fn get_invalid_key_error() -> PyErr {
        pyo3::exceptions::PyValueError::new_err("Invalid API key")
    }

    fn get_endpoint_not_compatible_error() -> PyErr {
        pyo3::exceptions::PyValueError::new_err("Endpoint is not compatible with model")
    }

    fn get_invalid_endpoint_error() -> PyErr {
        pyo3::exceptions::PyValueError::new_err("Invalid endpoint")
    }

    fn get_invalid_model_error() -> PyErr {
        pyo3::exceptions::PyValueError::new_err("Invalid model")
    }

    fn get_request_failed_error() -> PyErr {
        pyo3::exceptions::PyRuntimeError::new_err("Request failed for unknown reasons.")
    }
}

fn model_is_compatible(endpoint: &Endpoints, model: &Models) -> bool {
    if endpoint == &Endpoints::ChatCompletion {
        if [Models::Gpt3, Models::Gpt4].contains(model) {
            return true;
        } else {
            return false;
        }
    }
    
    else if endpoint == &Endpoints::Moderation {
        if [Models::ModerationStable, Models::ModerationLatest].contains(model) {
            return true;
        } else {
            return false;
        }
    }

    false
}

fn key_is_valid(api_key: &str) -> bool {
    if !api_key.starts_with("nv-") {
        return false;
    } else if !api_key.len() == 51 {
        return false;
    }

    true
}


#[pymodule]
fn nova_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Models>()?;
    m.add_class::<Endpoints>()?;
    m.add_class::<NovaClient>()?;
    Ok(())
}