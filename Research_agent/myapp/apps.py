from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'


# from langchain_openrouter import ChatOpenRouter

# model = ChatOpenRouter(
#     model="openai/gpt-4o-mini",
#     temperature=0.8,
# )

# # Example usage
# response = model.invoke("What NFL team won the Super Bowl in the year Justin Bieber was born?")
# print(response.content)