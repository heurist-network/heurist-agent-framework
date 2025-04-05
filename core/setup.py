from setuptools import setup

setup(
    name="heurist-core",
    version="0.1.0",
    package_dir={"heurist_core": "."},
    py_modules=["__init__", "embedding", "imgen", "llm", "voice", "videogen", "config"],
    packages=[
        "heurist_core",
        "heurist_core.components",
        "heurist_core.workflows",
        "heurist_core.tools",
        "heurist_core.utils",
        "heurist_core.heurist_image",
        "heurist_core.clients",
        "heurist_core.clients.search",
    ],
    install_requires=[
        "openai>=1.40.8",
        "requests>=2.31.0",
        "numpy>=1.26.3",
        "scikit-learn>=1.3.2",
        "psycopg2-binary>=2.9.9",
        "smolagents==1.9.2",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "tenacity>=8.5.0",
        "tiktoken>=0.5.2",
        "aiohttp>=3.9.3",
        "mcp>=0.1.0",
        "firecrawl>=0.1.0",
    ],
    python_requires=">=3.8",
)
