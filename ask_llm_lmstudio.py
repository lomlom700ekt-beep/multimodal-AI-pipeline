import requests

def ask_model(model, prompt, image_base64=None, timeout=120):
    url = "http://127.0.0.1:1234/v1/chat/completions"

    content = [{"type": "text", "text": prompt}]
    if image_base64 is not None:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_base64}"
            }
        })

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }

    response = requests.post(
        url,
        json=payload,
        timeout=timeout
    )
    response.raise_for_status()

    result = response.json()
    message = result["choices"][0]["message"]
    model_output = message.get("content") or message.get("reasoning_content", "")
    model_output = model_output.replace("```json", "").replace("```", "").strip()
    return model_output
