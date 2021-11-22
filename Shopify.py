import requests
import json
import dataset

class ShopifyScraper():

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def downloadjson(self, page):
        r = requests.get(self.baseurl + f'products.json?limit=250&page={page}', timeout=5)
        if r.status_code != 200:
            print('Bad Status Code: ', r.status_code)
        if len(r.json()["products"]) > 0:
            data = r.json()["products"]
            return data
        else:
            return

    def parsejson(self, jsondata):
        products = []
        for prod in jsondata:
            mainid = prod['id']
            title = prod['title']
            pub = prod['published_at']
            prodtype = prod['product_type']
            #print(prod['title'], prod['id'])
            for v in prod['variants']:
                item = {
                    'id': mainid,
                    'title': title,
                    'published_at': pub,
                    'product_type': prodtype,
                    'varid': v['id'],
                    'sku': v['sku'],
                    'price': v['price'],
                    'available': v['available'],
                    'created_at': v['created_at'],
                    'updated_at': v['updated_at'],
                    'compare_at_price': v['compare_at_price']
                }
                products.append(item)
        return products


def main():
    allbirds = ShopifyScraper('https://partakefoods.com/')
    results = []
    for page in range(1,10):
        data = allbirds.downloadjson(page)
        #print('Getting page', page)
        try:
            results.append(allbirds.parsejson(data))
        except:
            #print(f'Completed, total pages = {page-1}')
            break
    return results


if __name__ == '__main__':
    db = dataset.connect('sqlite:///products.db')
    table = db.create_table('foods', primary_id='varid')
    products = main()
    totals = [item for i in products for item in i]
    #print(len(totals))
    
    for pro in totals:
        if not table.find_one(varid=pro['varid']):
            table.insert(pro)
            print('New Product:',pro)