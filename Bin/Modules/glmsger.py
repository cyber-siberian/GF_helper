from Bin.Modules import gmailAPI
from Bin.Modules import logger
import datetime

date = (str(datetime.date.today().day) if datetime.date.today().day > 9
                else '0' + str(datetime.date.today().day)) + "." \
               + (str(datetime.date.today().month) if datetime.date.today().month > 9
                  else '0' + str(datetime.date.today().month)) + "." \
               + str(datetime.date.today().year)

class GLmsger():
    def __init__(self, ID, HTML=None):
        self.GMAIL = gmailAPI.gmailAPI(ID)
        self.LOGGER = None
        if HTML is not None:
            self.LOGGER = logger.Logger(HTML)

    " Transform new task-message from GlobalFreelance into dict"
    def glmsg_decoder(self, msg):
        msg = msg.split("Title:")
        title_cnt = '-'
        level_cnt = '-'
        deadl_cnt = '-'
        task_cnt = '-'
        try:
            title_cnt = msg[1].split('Level: ')[0]
            level_cnt = (msg[1].split('Level: ')[1]).split(' Deadline: ')[0]
            deadl_cnt = ((msg[1].split('Level: ')[1]).split('Deadline: ')[1]).split(' Task: ')[0]
            task_cnt = ((msg[1].split('Level: ')[1]).split(' Deadline: ')[1]).split(' Task: ')[1]
        except:
            pass
        decoded = {'NUMBER': '', 'TITLE': title_cnt, 'LEVEL': level_cnt, 'DEADLINE': deadl_cnt, 'TASK': task_cnt}
        return decoded

    " Searching for new task and filter (=delete) them if need it "
    def gltask_show_and_filter(self, filter_key=None, filter_word=None):
        new_task_msgs = self.GMAIL.find_msg('from: service@globalfreelance.ru is: unread +for evaluation')
        new_task_msgs += self.GMAIL.find_msg('from: service@globalfreelance.ru is: unread +UPDATED requirements')
        if new_task_msgs:
            for new_task_msg in new_task_msgs:
                new_task = self.GMAIL.get_msg(new_task_msg['id'])
                if new_task:
                    decoded_task = self.glmsg_decoder(new_task['snippet'])
                    decoded_task['NUMBER'] = new_task['payload']['headers'][16]['value'].split(",")[0].split(' ')[1]
                    if filter_key is not None and filter_word is not None and decoded_task[filter_key] == filter_word:
                        self.GMAIL.msg_to_thrash(new_task_msg['id'])
                        print("[+]The following message sent to trash:")
                        print("\t" + new_task['payload']['headers'][16]['value'] + " Reason -> " + decoded_task[filter_key] + " is in filter")
                    # else:
                        # print('\n[*] New Task!')
                        # print('\t(' + decoded_task['NUMBER'] + ')')
                        # print('\tTitle:    ' + decoded_task['TITLE'])
                        # print('\tLevel:    ' + decoded_task['LEVEL'])
                        # print('\tDeadline: ' + decoded_task['DEADLINE'])
                        # print('\tTask:     ' + decoded_task['TASK'])
        else:
            print("[.]No new tasks yet")

    " Delete tasks that are out of listing "
    def glexpired_filter(self):
        new_outofl_msgs = self.GMAIL.find_msg('from: noreply@globalfreelance.ru +out of listing')
        if new_outofl_msgs:
            for new_outofl_msg in new_outofl_msgs:
                new_outofl = self.GMAIL.get_msg(new_outofl_msg['id'])
                if new_outofl:
                    outofl_msg_tasknum = new_outofl['payload']['headers'][16]['value'].split(",")[0].split(" ")[1]
                    self.GMAIL.msg_to_thrash(new_outofl_msg['id'])
                    print("[+]The following message sent to trash:" + new_outofl['payload']['headers'][16]['value'])
                    all_task_msgs = self.GMAIL.find_msg('from: service@globalfreelance.ru +for evaluation')
                    if all_task_msgs:
                        for outofl_task in all_task_msgs:
                            expired_task_msg = self.GMAIL.get_msg(outofl_task['id'])
                            if expired_task_msg:
                                expired_task_num = expired_task_msg['payload']['headers'][16]['value'].split(",")[0].split(" ")[1]
                                if expired_task_num == outofl_msg_tasknum:
                                    self.GMAIL.msg_to_thrash(outofl_task['id'])
                                    print("[+]The following message sent to trash:" + expired_task_msg['payload']['headers'][16]['value'])
                                    if self.LOGGER is not None:
                                        self.LOGGER.set_task_missed(expired_task_num)
        else:
            print("[.]No expired tasks")

    " Find new quote messages "
    def glquote_find(self):
        new_quote_msgs = self.GMAIL.find_msg('from: service@globalfreelance.ru +quote received')
        if new_quote_msgs:
            for new_quote_msg in new_quote_msgs:
                new_quote = self.GMAIL.get_msg(new_quote_msg['id'])
                self.GMAIL.msg_to_thrash(new_quote_msg['id'])
                if new_quote:
                    try:
                        quote_msg_tasknum = new_quote['payload']['headers'][16]['value'].split(",")[0].split(" ")[1]
                        quote_msg_price = new_quote['snippet'].split(" for task")[0].split("your quote ")[1]
                        if self.LOGGER is not None:
                            self.LOGGER.set_new_task(quote_msg_tasknum, quote_msg_price)
                    except IndexError:
                        pass

    " Find done tasks "
    def gldone_find(self):
        new_done_msgs = self.GMAIL.find_msg('to: service@globalfreelance.ru +Completed')
        if new_done_msgs:
            for new_done_msg in new_done_msgs:
                new_done = self.GMAIL.get_msg(new_done_msg['id'])
                if new_done:
                    try:
                        done_msg_tasknum = new_done['payload']['headers'][3]['value'].split(",")[0].split(" ")[1]
                        self.GMAIL.msg_to_thrash(new_done['id'])
                        if self.LOGGER is not None:
                            self.LOGGER.set_task_done(done_msg_tasknum)
                    except IndexError:
                        pass

    " Delete old tasks "
    def glold_filter(self):
        new_old_msgs = self.GMAIL.find_msg('from: service@globalfreelance.ru +for evaluation')
        if new_old_msgs:
            for new_old_msg in new_old_msgs:
                new_old = self.GMAIL.get_msg(new_old_msg['id'])
                if new_old:
                    decoded_old = self.glmsg_decoder(new_old['snippet'])
                    task_date = decoded_old['DEADLINE'].split(' ')[0]
                    task_date = task_date.split('.')
                    cur_date = date.split('.')
                    if task_date[0] < cur_date[0] and task_date[1] <= cur_date[1] and task_date[2] <= cur_date[2]:
                        print("[+]Task " + decoded_old['NUMBER'] + " is outdated on " + str(decoded_old['DEADLINE'].split(' ')[0]))
                        self.GMAIL.msg_to_thrash(new_old_msg['id'])

    " Update HTML-file "
    def glupdate_html(self):
        if self.LOGGER is not None:
            self.LOGGER.update_html()
