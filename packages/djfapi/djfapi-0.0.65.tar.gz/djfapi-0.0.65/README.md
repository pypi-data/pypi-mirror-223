# djfapi

A utility library to integrate and use fastapi with the django orm.

## 🚧 This project is WIP and is subject to change at any time

This project is currently in the alpha state, even though it can be used in production with some caution. Make sure to fix the version in your requirements.txt and review changes frequently.

## Installation

`pip install djfapi`

## Features

### Sentry

Provides optional sentry integration.

### djdantic usage

See [djdantic](https://github.com/Voltane-EU/djdantic) for schema usage.

### Automatic Route Generation

Declare routes without having to write routes using the `djfapi.routing.django.DjangoRouterSchema`.

The `DjangoRouterSchema` will supply a router, which just has to be included in the FastAPI app.

#### Example for Routes

```python
from djfapi.routing.django import DjangoRouterSchema, SecurityScopes


transaction_token = JWTToken(scheme_name="Transaction Token")


def company_objects_filter(access: Access) -> Q:
    q = Q(tenant_id=access.tenant_id)
    if access.scope.selector != 'any':
        q &= Q(employees__user_id=access.user_id, employees__type__in=[models.Employee.EmployeeType.OWNER, models.Employee.EmployeeType.ADMIN])

    return q


router = DjangoRouterSchema(
    name='companies',
    model=models.Company,
    get=schemas.response.Company,
    create=schemas.request.CompanyCreate,
    update=schemas.request.CompanyUpdate,
    security=transaction_token,
    security_scopes=SecurityScopes(
        get=['business.companies.read.any', 'business.companies.read.own',],
        post=['business.companies.create',],
        patch=['business.companies.update.any', 'business.companies.update.own',],
        put=['business.companies.update.any', 'business.companies.update.own',],
        delete=['business.companies.delete.any', 'business.companies.delete.own',],
    ),
    objects_filter=company_objects_filter,
    children=[
        DjangoRouterSchema(
            name='departments',
            model=models.CompanyDepartment,
            get=schemas.response.CompanyDepartment,
            create=schemas.request.CompanyDepartmentCreate,
            update=schemas.request.CompanyDepartmentUpdate,
            children=[
                DjangoRouterSchema(
                    name='teams',
                    model=models.CompanyDepartmentTeam,
                    get=schemas.response.CompanyDepartmentTeam,
                    create=schemas.request.CompanyDepartmentTeamCreate,
                    update=schemas.request.CompanyDepartmentTeamUpdate,
                ),
            ]
        ),
        DjangoRouterSchema(
            name='costcenters',
            model=models.CompanyCostcenter,
            get=schemas.response.CompanyCostcenter,
            create=schemas.request.CompanyCostcenterCreate,
            update=schemas.request.CompanyCostcenterUpdate,
        ),
    ]
)
```
