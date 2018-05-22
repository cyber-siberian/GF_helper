from Bin.Modules import glmsger
from Bin.Modules.logger import Logger
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("[!]Usage: python ./main.py <email_address>")
        return 1
    else:
        if not os.path.exists('Log'):
            os.makedirs('Log')
        your_mailbox = sys.argv[1]
        print("[+]Specified email: " + your_mailbox)
        html_doc_path = os.getcwd() + '\Log\GL_log.htm'
        GlobalFreelance = glmsger.GLmsger(SCOPES='https://mail.google.com/',
                                          ID=your_mailbox,
                                          HTML=html_doc_path)
        GlobalFreelance.glexpired_filter()
        GlobalFreelance.gltask_show_and_filter()
        GlobalFreelance.glquote_find()
        GlobalFreelance.gldone_find()
        """ TEST """
        # log = Logger(html=html_doc_path)
        # log.update_html()

        return 0

if __name__ == '__main__':
    main()
