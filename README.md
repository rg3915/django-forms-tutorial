# django-forms-tutorial

Tutorial sobre formulários do Django para Live no YouTube.


## Este projeto foi feito com:

* [Python 3.9.4](https://www.python.org/)
* [Django 3.2.4](https://www.djangoproject.com/)


## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-forms-tutorial.git
cd django-forms-tutorial
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

Leia o [passo-a-passo.md](passo-a-passo.md)

![login.png](img/login.png)

---

![band_contact](img/band_contact.png)

