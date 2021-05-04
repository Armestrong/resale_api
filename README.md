<h1 align="center">Relase API imoveis</h1>

<h1 align="center">
    <a href="https://pt-br.reactjs.org/">:snake: Python</a>
</h1>
<p align="center">🚀 A technical proof with the purpose of this test is to develop a REST API to control the registration of properties and
real estate. that contain the listing, registration, edition and deletion.</p>



- Go to page [resale-api.herokuapp.com/](https://resale-api.herokuapp.com/api/user/create)

ENDPOINTS

Note: you need to be authenticated to use the API, if you prefer, use the [`ModHeader`](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj) google extension, to set your authentication Token

 - user
      - `api/user/create`
      - `api/user/token`
      - `api/user/me`
  
  
- imovel 
  - getAll 
    - `api/imovel/imoveis` 
    - `api/imovel/imobiliarias`
    
  - getById
    - `api/imovel/imoveis/{id}/`
    - `api/imovel/imobiliarias/{id}/`
  
  - Filtering imoveis by imobiliaria
    - `api/imovel/imoveis/imobiliarias/?real_estates={id}/`
  
  - Filtering imobiliarias that have been assigned with a imovel
    - `api/imovel/imoveis/imobiliarias/?assigned_only=1`
  
  - POST, PUT, PATCH and DELETE

### It was used:
 - Python
 - Django
 - Django Rest Framework
 - Docker
 - PostgreSQL
 - Travis-C
 - Heroku
