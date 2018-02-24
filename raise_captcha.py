from grab import Grab
from solve_captchas_with_model import get_capcha

g = Grab()
g.setup(reuse_cookies=True, debug=True)
store = []
vends = []


def get_img(h):
    alter = Grab()
    alter.cookies.load_from_file('cook.json')
    alter.setup(reuse_cookies=True, debug=True, headers=h)
    alter.go('https://elmir.ua/inc/CaptchaSecurityImages.php?width=110&height=60&characters=4')
    #print(alter.request_headers)
    f = open('ccc.jpg', 'wb')
    f.write(alter.doc.body)


def solve_captcha(somefunc):
    def exec_input_func(*args):
        if args:
            somefunc(args[0])
        else:
            somefunc()
        b = g.doc.select('//html').html()
        if u'подтвердите, что вы не бот' in b:
            hdrs = g.request_headers
            g.cookies.save_to_file('cook.json')
            print('I AM (not?) BOT!')
            while True:
                get_img(hdrs)
                res = get_capcha()
                if res:
                    print(res)
                    g.doc.set_input('captcha', res)
                    g.doc.submit()
                    exec_input_func(args[0]) if args else exec_input_func()
                    break
    return exec_input_func


@solve_captcha
def get_vendors():
    g.go('https://elmir.ua/voltage_regulators/')
    for i in g.doc.select('//ul[@id="list-0"]/li/a'):
        vends.append({'name': i.text(), 'url': i.select('@href').text()})


@solve_captcha
def get_products(url):
    g.go(url['url'])
    for el in g.doc.select('//ul[@id="vitrina-tovars"]/li/section'):
        stab = {
            'name': el.select('p[@class="name"]/a').text(),
            'url': el.select('p[@class="name"]/a/@href').text(),
            'price': el.select('div[@class="links"]/span[@class="price cost"]|div[@class="buy"]/div/span/span').text(),
            'vendor': url['name']
        }
        store.append(stab)
        print(stab)


if __name__ == '__main__':
    get_vendors()
    for k in vends:
        print(k)
        get_products(k)





