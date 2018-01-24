class GraphQLCompiledDocument(object):
    @classmethod
    def from_code(cls, schema, code, uptodate=None, extra_namespace=None):
        """Creates a GraphQLQuery object from compiled code and the globals.  This
        is used by the loaders and schema to create a template object.
        """
        namespace = {'__file__': code.co_filename}
        exec (code, namespace)
        if extra_namespace:
            namespace.update(extra_namespace)
        rv = cls._from_namespace(schema, namespace)
        rv._uptodate = uptodate
        return rv

    @classmethod
    def from_module_dict(cls, schema, module_dict):
        """Creates a template object from a module.  This is used by the
        module loader to create a template object.
        """
        return cls._from_namespace(schema, module_dict)

    @classmethod
    def _from_namespace(cls, schema, namespace):
        t = object.__new__(cls)
        t.schema = schema
        t.execute_func = namespace['execute']
        t._module = None
        t._uptodate = None

        # store the reference
        namespace['schema'] = schema
        namespace['__graphql_query__'] = t
        return t

    def execute(self, *args, **kwargs):
        return self.execute_func(*args, **kwargs)