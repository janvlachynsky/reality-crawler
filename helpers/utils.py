

class Utils:
    @staticmethod
    def parse_ad_id(url):
        """Returns ad id from url

        Args:
            url (_string_): url from Bazos ad

        Returns:
            _string_: adId
        """
        return url.split('/')[-2]
