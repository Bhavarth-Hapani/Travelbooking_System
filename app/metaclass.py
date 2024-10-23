# class ServiceMeta(type):
#     """
#     Metaclass to automatically register each subclass of travel services
#     (e.g., Flight, Hotel, Package) into a registry.
#     """
#     registry = {}

#     def __new__(mcs, name, bases, attrs):
#         cls = super().__new__(mcs, name, bases, attrs)
#         if name not in ['BaseService']:  # Exclude base class
#             # Register only subclasses, not BaseService itself
#             ServiceMeta.registry[name] = cls
#         return cls

#     @classmethod
#     def list_registered_services(cls):
#         """List all registered travel service models."""
#         return cls.registry

#     @classmethod
#     def get_service(cls, service_name):
#         """Retrieve a service model by its name."""
#         return cls.registry.get(service_name, None)
