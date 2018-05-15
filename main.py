from Bin.Modules import glmsger
import sys


def main():
    if len(sys.argv) != 1:
        print("[!]Usage: python main.py <email_address>")
        return 1
    else:
        your_mailbox = sys.argv[0]
        print("[+]Specified email: " + your_mailbox)
        excel_doc_path = 'Log/GL_log.xlsx'
        GlobalFreelance = glmsger.GLmsger(SCOPES='https://mail.google.com/',
                                          ID=your_mailbox,
                                          EXCEL=excel_doc_path)
        GlobalFreelance.glexpired_filter()
        GlobalFreelance.gltask_show_and_filter()
        GlobalFreelance.glquote_find()
        GlobalFreelance.gldone_find()
        return 0


if __name__ == '__main__':
    main()
