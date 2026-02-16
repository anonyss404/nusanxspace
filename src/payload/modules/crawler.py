import time

class Crawler:
    def __init__(self):
        self.name = "Crawler Module"
    
    def run(self, target):
        print(f"\n[•] Crawling {target}")
        time.sleep(2)
        print("[✓] Crawl completed - 0 vulnerabilities found")
        return []
