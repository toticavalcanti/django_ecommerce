def get_client_ip(request):
    # Obtém o valor do cabeçalho 'HTTP_X_FORWARDED_FOR' do objeto 'request.META'.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    # Verifica se o cabeçalho 'HTTP_X_FORWARDED_FOR' está presente.
    if x_forwarded_for:
        # Se estiver presente, o cabeçalho pode conter uma lista de endereços IP separados por vírgulas.
        # Portanto, dividimos a string em uma lista usando ',' como delimitador e pegamos o primeiro elemento da lista,
        # que é o endereço IP do user.
        ip = x_forwarded_for.split(",")[0]
    else:
        # Se o cabeçalho 'HTTP_X_FORWARDED_FOR' não estiver presente, usamos o endereço IP do user
        # que está disponível em 'request.META["REMOTE_ADDR"]'.
        ip = request.META.get("REMOTE_ADDR")
    
    # Retornamos o endereço IP final.
    return ip