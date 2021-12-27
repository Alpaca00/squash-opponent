

class UserAccount:
    class Opponent:
        phone = '+380634329876'
        district = 'Sychivskyi'
        category = 'PRO'
        datetime_ = '2022-01-20T18:00'
        exp_res = 'Successfully. Your post has been added.'
        endpoint = '/account/'

    class Tournament:
        title = 'Lviv getshirty tour'
        phone = '+380634329877'
        district = 'Sychivskyi'
        quantity_member = '7'
        category = 'PRO'
        datetime_ = '2022-01-20T19:00'
        exp_res = 'Successfully. The tournament has been created.'
        endpoint = '/account/tournaments'

    class FinderOpponent:
        name = 'John Doe'
        email = 'johndoetest0987@neo.com'
        phone = '+380630000002'
        district = 'Sychivskyi'
        category = 'PRO'
        message = '!hola amigo'
        datetime_ = '2022-01-20T18:00'
        exp_res = 'Successfully. Your post has been added.'
        endpoint = '/finder/'

    class ActionOpponent:
        exp_res_delete = 'Successfully. Your post has been deleted.'