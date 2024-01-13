from pydantic import Field, field_validator, ValidationError, BaseModel

class APIServer(BaseModel):
    proto: str = Field(default="http", description="Protocol")
    url: str = Field(default="127.0.0.1", description="Remote host request URL")
    port: int = Field(default=8000, description="Remote host port")
    api_str: str = Field(default="/api/v1", description="API endpoint, i.e. /api/v1")
    
    @property
    def base_url(self) -> str:
        """Base request URL."""
        _url: str = f"{self.proto}://{self.url}:{self.port}"
        
        return _url
    
    @property
    def healthcheck_url(self) -> str:
        """Healtcheck."""
        _url: str = f"{self.base_url}/health"
        
        return _url
    
    @field_validator("proto")
    def validate_prototype(cls, v) -> str:
        valid_protos: list[str] = ["http", "https"]
        
        if not v in valid_protos:
            raise ValueError(f"Invalid protocol: {v}. Must be one of {valid_protos}")

