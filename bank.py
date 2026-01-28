class Bank:
    def __init__(self, name, country, established_year):
        self.name = name
        self.country = country
        self.established_year = established_year

    def get_bank_info(self):
        return {
            "name": self.name,
            "country": self.country,
            "established_year": self.established_year
        }