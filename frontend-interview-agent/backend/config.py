import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DATABASE = os.path.join(basedir, 'interview_agent.db')
    DEBUG = False
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:3001']

    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'mock')
    AI_API_KEY = os.environ.get('AI_API_KEY', '')
    AI_BASE_URL = os.environ.get('AI_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
    AI_MODEL = os.environ.get('AI_MODEL', 'glm-4-flash')
    AI_TIMEOUT = int(os.environ.get('AI_TIMEOUT', '30'))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
