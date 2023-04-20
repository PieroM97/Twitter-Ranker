from trafilatura.settings import use_config
import trafilatura


config = use_config()
config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")

def getSinglePage(url):
    downloaded = trafilatura.fetch_url(url)
    output = trafilatura.extract(downloaded, config=config)
    return output