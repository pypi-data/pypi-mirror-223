# nova-python
🐍 Python library for accessing the Nova API

## Usage ##
Install the module (This requires <a href="https://rustup.rs/">Cargo</a>)  
```sh
$ pip install nova-python
```

Import the module
```python
from nova_python import Endpoints, Models, NovaClient
```

Create an instance of NovaClient, using your API key

```python
client = NovaClient("YOUR_API_KEY")
```

nova_python currently implements two enums: Endpoints and Models. Those contain:

**Endpoints**
* `Endpoints.CHAT_COMPLETION`
* `Endpoints.MODERATION`

**Models**
* `Models.GPT3`
* `Models.GPT4`
* `Models.MODERATION_LATEST`
* `Models.MODERATION_STABLE`  

Now, to make a request, use the `make_request` function. For example:

```python
from nova_python import Endpoints, Models, NovaClient
client = NovaClient("YOUR_API_KEY")

client.make_request(
    endpoint=Endpoints.CHAT_COMPLETION,
    model=Models.GPT3,
    data=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

or

```python
from nova_python import Endpoints, Models, NovaClient
client = NovaClient("YOUR_API_KEY")

client.make_request(
    endpoint=Endpoints.MODERATION,
    model=Models.MODERATION_STABLE,
    data=[{"input": "I'm going to kill them."}]
)
```


If everything goes to plan, you'll receive a string containing JSON-Data, which you can then use in your project.  
*Happy prompting!*

## FAQ ##
**Q:** I get an error when installing the package  
**A:** Make you sure, that you have <a href="https://rustup.rs/">Cargo</a> installed

Made with 🩸 by Leander