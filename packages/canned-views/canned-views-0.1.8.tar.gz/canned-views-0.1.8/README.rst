Canned Views
------------

Views, as in SQL views.

SQL views presented as simple Django ListView reports rendered by DataTables.

Overview
========

The online report renders from the results of an SQL VIEW using ``DataTables``.

* Each report is defined in the model ``CannedViews``;
* The SQL VIEW must exist in the DB and the name must be prefixed with ``canned_``;
* The rendered report is limited to 500 records for now. If the query returns more than 500 records, the report will only render the first 500 in the order of the query;
* You can specify one column to render as a hyperlink. In almost all cases this will be the ``subject_identifier`` column.

Rendering one column as a url
=============================

To reverse a url, include the columns by name separated by commas in the ``reverse_url_args`` column. It is up to you to ensure that the ``reverse_url_name`` is valid and in the global dictionary ```url_names```.

