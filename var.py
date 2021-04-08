
PATH = "./data/export_data.csv"

COL_NAME = [ 'annee',
             'year_month',
             'id_intervention',
             'categorie_age_adulte',
             'age',
             'poids',
             'taille',
             'asa',
             'urgence',
             'sexe',
             'lib_diagnostic',
             'service',
             'rea_post_op',
             'duree_rea_post_op',
#              'curare_i',
#              'curare',
#              'admin_desflurane',
#              'admin_sevoflurane',
#              'halogene_administre',
#              'admin_halogenes',
#              'dobutamine',
#              'total_dobutamine',
#              'ephedrine',
#              'total_ephedrine',
#              'gelofusine',
#              'total_gelofusine',
#              'hea',
#              'total_hea',
#              'noradrenaline',
#              'total_noradrenaline',
#              'phenylephrine',
#              'total_phenylephrine',
#              'ringer',
#              'total_ringer',
#              'ringer_lactate',
#              'total_ringer_lactate',
#              'serum_sale',
#              'total_serum_sale',
#              'total_remplissage' 
           ]

"""
month = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jui", "Aou", "Sep", "Oct", "Nov", "Dec"]
month_convert = dict([(name, str(num+1).rjust(2,"0")) for name, num in zip(month, range(len(month)))])
"""
MONTH_CONVERT = {'Jan': '01',
                 'Fev': '02',
                 'Mar': '03',
                 'Avr': '04',
                 'Mai': '05',
                 'Jun': '06',
                 'Jui': '07',
                 'Aou': '08',
                 'Sep': '09',
                 'Oct': '10',
                 'Nov': '11',
                 'Dec': '12'
                }
