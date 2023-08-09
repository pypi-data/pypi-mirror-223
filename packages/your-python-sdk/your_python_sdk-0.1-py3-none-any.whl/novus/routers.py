class CustomRouter(object):
    route_novus_labels = {
        # django
        "sessions",
        "admin",
        "sites",
        "auth",
        "contenttypes",
        # end django
        "log",
        "country",
        "region",
        "category",
        "area",
        "role",
        "user",
        "type_process",
        "type_process_mail",
        "status_process",
        "status_process_tran",
        "status_process_mail",
        "process",
        "process_tran",
        "process_mov",
        "process_act",
        "process_mail",
    }

    route_fehu_labels = {
        "client",
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_novus_labels:
            return "default"
        if model._meta.app_label in self.route_fehu_labels:
            return "fehu"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_novus_labels:
            return "default"
        if model._meta.app_label in self.route_fehu_labels:
            return "fehu"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_novus_labels
            and obj2._meta.app_label in self.route_novus_labels
        ):
            return True
        if (
            obj1._meta.app_label in self.route_fehu_labels
            and obj2._meta.app_label in self.route_fehu_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_novus_labels:
            return db == "default"
        if app_label in self.route_fehu_labels:
            return db == "fehu"
        return None
