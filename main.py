# import tabula
# from tabulate import tabulate
# import pandas as pd

# # Read tables from the PDF
# tables = tabula.read_pdf("index.pdf", pages='all', multiple_tables=True)

# # Prepare data for output
# output_data = []

# current_institute_code = ""
# current_institute_name = ""

# for i, table in enumerate(tables):
#     print(i)
#     # Check if this table contains institute information
#     if table.shape[1] == 1 and table.iloc[0, 0].strip().split()[0].isdigit():
#         institute_info = table.iloc[0, 0].strip().split(maxsplit=1)
#         current_institute_code = institute_info[0]
#         current_institute_name = institute_info[1]
#         continue

#     # Process course information
#     if 'Choice Code' in table.columns and 'Course Name' in table.columns:
#         choice_code = table['Choice Code'].iloc[0].split()[-1]
#         course_name = table['Course Name'].iloc[0]

#         # Find GOPEN data
#         if 'GOPEN' in table.columns:
#             gopen_data = table['GOPEN'].iloc[0].split()
#             if len(gopen_data) >= 2:
#                 gopen_Number = gopen_data[0]
#                 gopen_Percent = gopen_data[1].strip('()')

#                 output_data.append([
#                     current_institute_code,
#                     current_institute_name,
#                     choice_code,
#                     course_name,
#                     gopen_Number,
#                     gopen_Percent
#                 ])

# # Create a DataFrame from the extracted data
# df = pd.DataFrame(output_data, columns=['Institute Code', 'College Name', 'Choice Code', 'Course Name', 'GOPEN Number', 'GOPEN Percent'])

# # Remove duplicate rows
# df = df.drop_duplicates()

# # Sort the DataFrame by Institute Code and Choice Code
# df = df.sort_values(['Institute Code', 'Choice Code'])

# # Save to CSV
# df.to_csv('extracted_data.csv', index=False)

# # Print the table to console
# print(tabulate(df, headers='keys', tablefmt='pipe', showindex=False))

# print("\nData has been extracted and saved to 'extracted_data.csv'")


# from tabula import read_pdf
# from tabulate import tabulate
 
# #reads table from pdf file
# df = read_pdf("index.pdf",pages="all",multiple_tables=True) #address of pdf file
# # for row in df:
# #     print(row)
# print(df[5])


# only works GOPEN
import pandas as pd
import pdfplumber
main_df = pd.DataFrame(columns=['College Code',
                                    'College Name',
                                    'College Type',
                                    'Choice Code',
                                    'Course Name',
                                    'Stage',
                                    'Category',
                                    'Number',
                                    'Percent',
                                    ])
# current dict
dict = {}
for key in main_df.keys():
    dict[key] = ""
print(dict)
with pdfplumber.open("index.pdf") as pdf:
    for page in pdf.pages:
        tables=page.extract_tables()
        for (i,table) in enumerate(tables):
            # print(table)
            if(i%2==0):

                # current_df['College Name'] = table[0][0]
                # print(current_df)
                # current_df.iloc[0:, 'College Name'] = table[0][0]
                dict={
                    "College Code":table[0][0].split(" ")[0],
                    "College Name":table[0][0].split(" ",1)[1],
                    "College Type":table[0][0][::-1].split("( ")[0].split(")",1)[1][::-1],
                    "Choice Code":table[1][1],
                    "Course Name":table[1][3],
                }

                # print(current_df)
                # print(dict)
            else:
                columns=["Stage"]+(table[0][1:])
                df=pd.DataFrame(table[1:],columns=columns)
                table2=df.transpose().to_dict().values()
                for row_dict in table2:
                    # print(row_dict)
                    stage=row_dict["Stage"]
                    for category in list(row_dict.keys())[1:]:
                        if row_dict[category].strip() == '':
                            continue
                        number=row_dict[category].split("\n")[0]
                        # print("n",number)
                        percent=row_dict[category].split("\n")[1][1:-1]
                        print("p",percent)
                        dict["Stage"]=stage
                        dict["Category"]=category
                        dict["Number"]=number
                        dict["Percent"]=percent
                        # print(dict)

                        main_df = pd.concat([main_df, pd.DataFrame(dict, index=[0])], ignore_index=True)
                        # main_df=main_df.append(dict, ignore_index = True)




# {'Stage': {0: 'Stage-I', 1: 'Stage-II'}, 'GOPEN': {0: '5763\n(84.53%)', 1: ''}, 'GSC': {0: '21286\n(75.05%)', 1: ''}, 'GST': {0: '35049\n(68.11%)', 1: ''}, 'GOBC': {0:
#  '10971\n(80.53%)', 1: ''}, 'LNTA': {0: '', 1: '24953\n(73.37%)'}, 'LOBC': {0: '2945\n(87.68%)', 1: ''}, 'PWD-O': {0: '23893\n(73.84%)', 1: ''}, 'DEF-O': {0: '35968\n(
# 67.45%)', 1: ''}, 'EWS': {0: '36441\n(67.11%)', 1: ''}}

main_df.to_csv("extracted_data.csv", index=False)
