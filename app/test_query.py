from app.models.contact import Contact

pagination = Contact.query.filter_by(user_id=2).paginate(page=1, per_page=5)

i = 0

for page_num in pagination.iter_pages():
    print('PAGE:', pagination.page)
    print('====')
    for contact in pagination.items:
        i =+ 1
        print(i)
        print(contact, '| name: ', contact.name)
    print('-'*20)
    pagination = pagination.next()
