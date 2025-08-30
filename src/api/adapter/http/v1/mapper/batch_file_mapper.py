class BatchFileMapper:

    def build_batch_file_content(self, model_name: str, content: list, url: str):
        for idx, data in enumerate(content):
            yield self.__build_batch_line(
                custom_id=f"{idx}",
                url=url,
                model=model_name,
                data=data,
            )

    def __build_batch_line(self, custom_id: str, url: str, model: str, data: list):
        return {
            "custom_id": custom_id,
            "method": "POST",
            "url": url,
            "body": {
                "model": model,
                "messages": data.get("messages", []),
                "max_tokens": data.get("max_tokens", 0),
            },
        }
