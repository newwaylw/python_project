from robobrowser import RoboBrowser
import time
import os.path
import datetime
import logging
import random

prefer_times = list()

prefer_times.append(1541246400)  # 11/03/2018 @ 12:00pm (UTC)
prefer_times.append(1541250000)   # 11/03/2018 @ 1:00pm (UTC)
prefer_times.append(1541332800)   # 11/04/2018 @ 12:00pm (UTC)
prefer_times.append(1541336400)  # 11/04/2018 @ 1:00pm (UTC)
prefer_times.append(1541264400)   # 11/03/2018 @ 5:00pm (UTC)
prefer_times.append(1541268000)  # 11/03/2018 @ 6:00pm (UTC)
prefer_times.append(1541350800)
prefer_times.append(1541354400)

BOOKING_URL = 'http://dongree.xsrv.jp/kichikichi/reserve/booking-form/?aid={}&utm={}'
EMAIL = 'mrs_b.hu@outlook.com'
LOCK_FILE = '.booking_success'

error_types = ['Success', 'Reservation ended','Reservation not accepted',
               'Outside reservation period', 'We do not accept reservations now', 'capacity over', 'unknown']

user_agents = ['Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
               'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9']

script_dir = os.path.dirname(os.path.realpath(__file__))
log_file = os.path.join(script_dir, 'kichi2_booking.log')
logging.basicConfig(filename=log_file, level=logging.INFO)


def make_booking(url, num_people, lead_name, hotel_name, email, country, tel):

    logging.info('[%s] requesting %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), url))
    browser = RoboBrowser(history=False, user_agent=random.choice(user_agents))
    browser.open(url)

    # some error handling
    err = browser.select('div.error-message')
    if len(err) > 0:
        if '指定日時の予約受け付けは終了しました。' in str(err[0]):
            return 1  # 'Reservation ended'
        elif '指定時間は予約を受け付けておりません' in str(err[0]):
            return 2  # Reservation not accepted
        elif '予約受付期間外です' in str(err[0]):
            return 3  # Outside reservation period
        elif 'ただ今予約は受け付けておりません' in str(err[0]):
            return 4  # We do not accept reservations now.
        else:
            return 6  # unknown error

    form = browser.get_form()

    # fill form
    form['booking[client][adult]'].value = num_people
    form['booking[client][name]'].value = lead_name
    form['booking[client][company]'].value = hotel_name
    form['booking[client][email]'].value = email
    form['booking[client][email2]'].value = email
    form['booking[client][country]'].value = country
    form['booking[client][tel]'].value = tel
    browser.submit_form(form)

    print(browser.parsed)

    err = browser.select('div.error-message')
    if len(err) > 0 and '定員オーバーのため予約不可です' in str(err[0]):
        return 5  # capacity over
        # get pass confirmation page
    form2 = browser.get_form()
    #     json2 = form2.serialize()
    browser.submit_form(form2)

    return 0  # success!


def main():
    success = False
    delay = 1

    if os.path.isfile(LOCK_FILE):
        logging.info('[%s] already succeed, program stopped. to run, please delete file: %s' %
                     (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), LOCK_FILE))
        exit(0)

    for t in prefer_times:
        dt = datetime.datetime.utcfromtimestamp(t)
        hour = dt.hour

        if hour in [12, 13]:  # Lunch
            aid = 17
        else:
            aid = 6

        url = BOOKING_URL.format(aid, t)
        ret = make_booking(url, '4', 'Baoqing Hu', 'N/A', EMAIL, 'UK', '00447875643636')
        if ret == 0:
            success = True
            break

        logging.info('[%s] booking failed, reason=%s' % (
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), error_types[ret]))

        time.sleep(delay)  # Wait a bit

    if success:
        msg = '[%s] booking successful, check %s for confirmation' % (
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), EMAIL)
        logging.info(msg)
        with open('.booking_success', 'w') as f:
            f.write(msg)


if __name__ == "__main__":
    main()

