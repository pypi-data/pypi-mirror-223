from typing import Dict, Any, Optional


class PolicyDocument:
    """
    Policy document that is constructed according to this documentation:
    https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html
    """
    def __init__(
            self,
            region: str,
            account_id: str,
            api_id: str,
            api_key: Optional[str] = None
    ) -> None:
        self.region = region
        self.account_id = account_id
        self.api_id = api_id
        self.api_key = api_key

    def create_policy_statement(
            self,
            allow: bool = False
    ) -> Dict[str, Any]:
        return {
            'principalId': 'user',
            'context': {
                'ApiKey': self.api_key
            },
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Resource': f'arn:aws:execute-api:{self.region}:{self.account_id}:{self.api_id}/*/*',
                        'Effect': 'Allow' if allow else 'Deny'
                    }
                ]
            }
        }
