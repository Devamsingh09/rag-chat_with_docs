def handle_chat(user_query, chain):
    response = chain.invoke(user_query)
    return response
