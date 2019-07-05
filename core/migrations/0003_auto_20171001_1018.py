from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("core", "0002_invoice_note")]

    operations = [
        migrations.RemoveField(model_name="invoice", name="client"),
        migrations.RemoveField(model_name="invoice", name="entries"),
        migrations.RemoveField(model_name="invoice", name="site"),
        migrations.RemoveField(model_name="client", name="invoice_email"),
        migrations.DeleteModel(name="Invoice"),
    ]
