import flags
from service.google import GoogleService

def main():
  content = "Hello World"
  if flags.flags().email:
    GoogleService().send_mail(content)

if __name__ == '__main__':
  main()