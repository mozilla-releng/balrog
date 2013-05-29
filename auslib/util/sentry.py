from raven.processors import Processor

class SanitizeHeadersProcessor(Processor):
    sanitizeHeaders = ['Authorization']

    def process(self, data):
        data = data['sentry.interfaces.Http']
        if 'headers' in data:
            for header in self.sanitizeHeaders:
                if header in data['headers']:
                    data['headers'][header] = 'REDACTED'
        return data
