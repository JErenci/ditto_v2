import sys, os, base64

company_name = 'Vaude'
# company_name = 'D1tt0'
company_name = 'Baumgartner'

logging_Home = True
logging_Company = False
logging_Products = False
logging_Customers = False

################################################

file_used = f'./data_loaded_{company_name}.json'

################################################
if logging_Home:
    print(f'company={company_name}')
    print(f'file_used={file_used}')

companyLogo = 'logo.jpg'
companyUser = 'user.jpg'

filename_without_extension = '1_Home'#os.path.basename(__file__).split('.')[0]
print(f'filename_without_extension={filename_without_extension}')

path_to_default_companyLogo = f'./assets/{company_name}/{filename_without_extension}/{companyLogo}'
path_to_default_companyUser = f'./assets/{company_name}/{filename_without_extension}/{companyUser}'

print(f'path_to_default_companyLogo={path_to_default_companyLogo}')
print(f'path_to_default_companyUser={path_to_default_companyUser}')
base64_decoded_company_image = base64.b64encode(open(path_to_default_companyLogo, "rb").read()).decode()
base64_decoded_user_image = base64.b64encode(open(path_to_default_companyUser, "rb").read()).decode()

img_logo = base64_decoded_company_image
img_user = base64_decoded_user_image
