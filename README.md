<h1 align="center">Relase API imoveis</h1>

<h1 align="center">
    <a href="https://pt-br.reactjs.org/">:snake: Python</a>
</h1>
<p align="center">🚀 A technical proof with the purpose of this test is to develop a REST API to control the registration of properties and
real estate. that contain the listing, registration, edition and deletion.</p>


![Badge](resale-api.herokuapp.com/API-RESTFULL-%237159c1?style=for-the-badge&logo=ghost)

- Go to page - ``
- [resale-api.herokuapp.com/](https://resale-api.herokuapp.com/)

ENDPOINTS

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


