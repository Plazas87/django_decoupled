# Django decoupled

This is proposal for implementing hexagonal architecture in conjunction with Django. The main challenge lies in Django's inclusion of numerous features and functionalities, which can be advantageous but also limits control over the underlying processes.

When considering a Django project with a layered architecture, there are a few complexities to navigate. By default, Django allows importing domain models from anywhere, leading to frequent violations of the layered structure. Additionally, the way Django loads apps can present issues in certain cases. Finally, figuring out the proper functioning of Django signals poses a more complex challenge that I am currently attempting to address.
