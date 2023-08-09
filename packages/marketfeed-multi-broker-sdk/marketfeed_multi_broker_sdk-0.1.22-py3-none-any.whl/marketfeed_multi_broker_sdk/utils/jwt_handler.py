import jwt

# JWT secret key
JWT_SECRET = 'multi-broker-sdk-secret'


def jwt_encode(payload):
    """
    This function encodes the payload into a JWT

    Args:
        payload (dict): A dictionary containing the payload data

    Returns:
        str: The encoded JWT as a string
    """
    try:
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    except Exception as e:
        raise Exception(f"Error encoding JWT: {str(e)}")


def jwt_decode(token):
    """
    This function decodes the token into a payload

    Args:
        token (str): A JWT string

    Returns:
        dict: The decoded payload as a dictionary
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise Exception("Error: Signature has expired")
    except jwt.InvalidTokenError:
        raise Exception("Error: Invalid Token")
    except Exception as e:
        raise Exception(f"Error decoding JWT: {str(e)}")
