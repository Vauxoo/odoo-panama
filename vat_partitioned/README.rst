Partitioned VAT
===============


        vat_partitioned

        This module splits the VAT field into 3 fields:
            1. vat_country_id (Country to form VAT)
            2. vat_alone (Only VAT value)
            3. vat_dv (Check digit)

        The previous fields will be disposed to replace the directly
        'VAT' field editing.
