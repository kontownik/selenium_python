import collections

Account = collections.namedtuple('Account', 'email password name user_type')

user = Account(email='demo+111@demo.com', password='Demo123', name='Paweł', user_type='end-user')
admin = Account(email='demo@demo.com', password='Demo123', name='Paweł', user_type='organization-admin')
user_change_email = Account(email='demo+5@demo.com', password='Demo123', name='Paweł', user_type='end-user-email-change')
