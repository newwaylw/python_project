from robobrowser import RoboBrowser
import time
import os.path
import datetime
import logging

prefer_times = list()

prefer_times.append(1541246400) # 11/03/2018 @ 12:00pm (UTC)
prefer_times.append(1541250000)   # 11/03/2018 @ 1:00pm (UTC)
prefer_times.append(1541332800)   # 11/04/2018 @ 12:00pm (UTC)
prefer_times.append(1541336400)  # 11/04/2018 @ 1:00pm (UTC)
prefer_times.append(1541264400)   # 11/03/2018 @ 5:00pm (UTC)
prefer_times.append(1541268000)  # 11/03/2018 @ 6:00pm (UTC)
prefer_times.append(1541350800)
prefer_times.append(1541354400)

BOOKING_URL = 'http://dongree.xsrv.jp/kichikichi/reserve/booking-form/?aid=6&utm='
EMAIL = 'mrs_b.hu@outlook.com'
LOCK_FILE = '.booking_success'

error_types = ['Success', 'Reservation ended','Reservation not accepted',
               'Outside reservation period', 'We do not accept reservations now', 'capacity over', 'unknown']

logging.basicConfig(filename='booking.log', level=logging.INFO)


def make_booking(url, num_people, lead_name, hotel_name, email, country, tel):

    logging.info('[%s] requesting %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), url))
    browser = RoboBrowser(history=False, user_agent='Mozilla/5.0 (X11; Linux x86_64)')
    browser.open(url)

    # some error handling
    err = browser.select('div.entry-content')
    if len(err) > 0 and '指定日時の予約受け付けは終了しました。' in str(err[0]):
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
    inc = 2
    delay = 5

    if os.path.isfile(LOCK_FILE):
        logging.info('[%s] already succeed, program stopped. to run, please delete file: %s' %
                     (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), LOCK_FILE))
        exit(0)

    for t in prefer_times:
        url = BOOKING_URL + str(t)
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

