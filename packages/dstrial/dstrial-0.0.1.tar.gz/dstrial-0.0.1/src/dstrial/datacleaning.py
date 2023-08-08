### importing the required packages
import numpy as np

# from scipy.stats import shapiro
from scipy.stats import skew
from scipy.stats import f_oneway
import scipy.stats as stats
import pandas as pd
import seaborn as sns
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


## classs initialization
class Datacleaning:
    def __init__(self):
        self.valid_extensions = ["csv", "xlsx", "json", "txt", "xls"]

    ## Reading the data from various file and data storages.
    def columns(self):
        return self.dataframe.columns

    def summary(self):
        return self.dataframe.describe(include="all")

    def read_data(self, input_dataset):
        if "." in input_dataset:
            self.file_extension = input_dataset.split(".")[-1].lower()
        else:
            self.file_extension = input_dataset.lower()

        if self.file_extension in self.valid_extensions:
            try:
                if self.file_extension == "csv":
                    self.dataframe = pd.read_csv(input_dataset)
                elif self.file_extension == "xlsx":
                    self.dataframe = pd.read_excel(input_dataset)
                elif self.file_extension == "xls":
                    self.dataframe = pd.read_excel(input_dataset)
                elif self.file_extension == "json":
                    self.dataframe = pd.read_json(input_dataset)
                elif self.file_extension == "txt":
                    self.dataframe = pd.read_csv(input_dataset, sep="\t")

                return self.dataframe.head()

            except Exception as e:
                print(f"An error occured while reading the file: {e}")
                return None

        else:
            print("Ïnvalid file extension. Cannot read the file with pandas")

    ## Looking at the structure of the data
    def head(self, number):
        if not number:
            print(self.dataframe.head(number))
        elif isinstance(number, int):
            print(self.dataframe.head(number))
        elif isinstance(number, float):
            print(self.dataframe.head(int(number)))
        else:
            print("Please Enter an integer or a floating point as parameter")

    ## getting the datafame
    def getdata(self):
        return self.dataframe

    ## Checking for the number of missing values
    def missing_values(self):
        return self.dataframe.isnull().sum()

    ## Col missing_values
    def col_missing_value(self, col_name):
        empty_value = self.dataframe[col_name].isnull().sum()
        return empty_value

    ## removing empty columns
    def remove_empty_columns(self):
        number_of_rows = self.dataframe.shape[0]
        empty_columns = [
            col
            for col in self.dataframe.columns
            if self.col_missing_value(col) == number_of_rows
        ]

        self.dataframe.drop(columns=empty_columns, inplace=True)

    ## grouping categorical and continuous data
    def data_types(self):
        self.categorical_data = self.dataframe.select_dtypes(include=["object"])
        self.continuous_data = self.dataframe.select_dtypes(exclude=["object"])

    ## Accessing categorical data
    def cat_cols(self):
        self.data_types()
        return self.categorical_data.head()

    ### Accessing continouos data
    def cont_cols(self):
        self.data_types()
        return self.continuous_data.head()

    ## visualising distributions of continious variables
    def distributions(self):
        self.remove_empty_columns()
        self.data_types()
        # self.cat_dist()
        num_columns = len(self.continuous_data.columns)
        num_rows = (num_columns + 2) // 3  # Calculate the number of rows dynamically
        
        if num_columns == 1:
            self.col_dist(self.continuous_data.columns[0])
        else:
            fig, axs = plt.subplots(num_rows, 3, figsize=(15, num_rows * 5))
            
            for i, col in enumerate(self.continuous_data.columns):
                
                row = i // 3
                col_idx = i % 3
                ax = axs[row, col_idx]
                ax.hist(self.dataframe[col])
                ax.set_title(f"Distribution of {col}")
            
            for i in range(num_columns, num_rows * 3):
                axs.flatten()[i].axis('off')
            
            plt.tight_layout()
            plt.show()

    ## visualising a single column
    def col_dist(self, col):
        plt.hist(self.dataframe[col], bins=10)
        plt.title(f"Distribution of {col}")
        plt.show
        
    ## Visualising categorical data
    def cat_dist(self):
        self.remove_empty_columns()
        self.data_types()
        num_columns = len(self.categorical_data.columns)
        num_rows = (num_columns + 2) // 3
        
        if num_columns == 1:
            self.col_cat_dist(self.categorical_data.columns[0])
        else:
            fig, axs = plt.subplots(num_rows, 3, figsize=(15, num_rows * 5))
            axs = axs.flatten()  # Flatten axs to ensure a 1D array
            
            for i, col in enumerate(self.categorical_data.columns):
                row = i // 3
                col_idx = i % 3
                ax = axs[i]  # Use the flattened array
                
                # Use FacetGrid context for sns.countplot
                with sns.axes_style("whitegrid"):
                    g = sns.countplot(data=self.dataframe, x=col, ax=ax)
                    g.set_title(f"Distribution of {col}")
                
            for i in range(num_columns, num_rows * 3):
                axs[i].axis("off")
            
            plt.tight_layout()
            plt.show()


    ## Visualising a single column
    def col_cat_dist(self, col):
        sns.displot(self.dataframe[col])
        plt.title(f"Distribution of {col}")
        plt.show()


    ## Dropping and removing missing values
    def remove_missingvalues(self):
        self.remove_empty_columns()
        self.dataframe = self.dataframe.drop_duplicates()
        self.data_types()
        for col_name in self.dataframe.columns:
            ## if a column is categorical
            if col_name in self.categorical_data.columns:
                self.dataframe[col_name].fillna(
                    self.dataframe[col_name].mode()[0], inplace=True
                )
            ## if a column is continuous
            elif col_name in self.continuous_data.columns:
                skewness = skew(self.continuous_data[col_name])
                if skewness > 0:
                    self.dataframe[col_name].fillna(
                        self.dataframe[col_name].median(), inplace=True
                    )
                elif skewness < 0:
                    self.dataframe[col_name].fillna(
                        self.dataframe[col_name].median(), inplace=True
                    )
                else:
                    self.dataframe[col_name].fillna(
                        self.dataframe[col_name].mean(), inplace=True
                    )

    ## dropping a columns
    def drop(self, column):
        if isinstance(column, list):
            self.dataframe = self.dataframe.drop(columns=column)
        else:
            self.dataframe = self.dataframe.drop(column, axis=1)

    ### Checking and visualising outliers through boxplots
    def outliers(self):
        self.data_types()
        num_cols = len(self.continuous_data.columns)
        nrows = (num_cols - 1) // 3 + 1
        ncols = min(num_cols, 3)
        if num_cols == 1:
            self.outliers_single(self.continuous_data.columns[0])
        else:
            plt.figure(figsize=(20, 20))
            for i, col in enumerate(self.continuous_data.columns):
                plt.subplot(nrows, ncols, i + 1)
                plt.boxplot(self.dataframe[col])
                plt.title(col)
            plt.tight_layout()
            plt.show()

    ## dealing with a single outlier
    def outliers_single(self, column):
        plt.figure(figsize=(10, 8))
        plt.boxplot(self.dataframe[column])
        plt.title(column)
        plt.tight_layout()
        plt.show()

    ### Removing outliers for categorical data through the inter-quatile range method
    def remove_outliers(self):
        self.data_types()
        for i in self.continuous_data.columns:
            lower_quantile = self.dataframe[i].quantile(0.25)
            upper_quantile = self.dataframe[i].quantile(0.75)
            IQR = upper_quantile - lower_quantile
            upper_boundary = upper_quantile + 1.5 * IQR
            lower_boundary = upper_quantile - 1.5 * IQR
            self.dataframe[i] = np.where(
                self.dataframe[i] > upper_boundary, upper_boundary, self.dataframe[i]
            )
            self.dataframe[i] = np.where(
                self.dataframe[i] < lower_boundary, lower_boundary, self.dataframe[i]
            )

    ### plotting a correlation matrix
    def corr_matrix(self):
        self.data_types()
        correlation_matrx = self.continuous_data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            correlation_matrx, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5
        )
        plt.title("Correlation Matrix")
        plt.show()

    ### a pair plot for visualizing scatter plots for continouos data.

    def cont_corr(self):
        self.data_types()
        sns.pairplot(self.continuous_data[self.continuous_data.columns])

    ## Relationship between continouos data between continouos data.
    def cont_to_cont(self, col1, col2):
        if isinstance(col1, str):
            if isinstance(col2, str):
                self.dataframe.plot.scatter(x=col1, y=col2, title=col1 + " vs " + col2)
                correlation_value = self.dataframe[col1].corr(self.dataframe[col2])
                print(
                    f"The correlation between {col1} and {col2} is: {correlation_value}"
                )

            elif isinstance(col2, list):
                for value in col2:
                    self.dataframe.plot.scatter(
                        x=col1, y=value, title=col1 + "vs" + value
                    )
                    correlation_value = self.dataframe[col1].corr(self.dataframe[value])
                    print(
                        f"The correlation between {col1} and {value} is: {correlation_value}"
                    )
            else:
                print("Enter a sting or a list as parameters for parameter two")
        elif isinstance(col1, list):
            if isinstance(col2, str):
                for value in col1:
                    self.dataframe.plot.scatter(
                        x=value, y=col2, title=value + "vs" + col2
                    )
                    correlation_value = self.dataframe[value].corr(self.dataframe[col2])
                    print(
                        f"The correlation between {value} and {col2} is: {correlation_value}"
                    )

            elif isinstance(col2, list):
                num_rows = len(col1)
                num_columns = len(col2)

                if num_rows == 1 and num_columns == 1:
                    self.dataframe.plot.scatter(
                        x=col1[0], y=col2[0], title=col1[0] + "vs" + col2[0]
                    )
                    correlation_value = self.dataframe[col1[0]].corr(
                        self.dataframe[col2[0]]
                    )
                    print(
                        f"The correlation between {col1[0]} and {col2[0]} is: {correlation_value}"
                    )

                elif num_rows == 1 and num_columns > 1:
                    for value in col2:
                        self.dataframe.plot.scatter(
                            x=col1[0], y=value, title=col1[0] + " vs " + value
                        )
                        correlation_value = self.dataframe[col1[0]].corr(
                            self.dataframe[value]
                        )
                        print(
                            f"The correlation between {col1[0]} and {value} is: {correlation_value}"
                        )

                elif num_rows > 1 and num_columns == 1:
                    for value in col1:
                        self.dataframe.plot.scatter(
                            x=value, y=col2[0], title=value + " vs " + col2[0]
                        )
                        correlation_value = self.dataframe[col2[0]].corr(
                            self.dataframe[value]
                        )
                        print(
                            f"The correlation between {col2[0]} and {value} is: {correlation_value}"
                        )

                    plt.tight_layout()

                elif num_rows > 1 and num_columns > 1:
                    fig, axes = plt.subplots(num_rows, num_columns, figsize=(20, 20))
                    for i, x in enumerate(col1):
                        for j, y in enumerate(col2):
                            ax = axes[i, j]
                            ax.scatter(self.dataframe[x], self.dataframe[y])
                            ax.set_xlabel(f"{col1[i]}")
                            ax.set_ylabel(f"{col2[j]}")
                            ax.set_title(f"Scatter Plot ({col1[i]} vs {col2[j]})")
                            correlation_value = self.dataframe[x].corr(
                                self.dataframe[y]
                            )
                            print(
                                f"The correlation between {x} and {y} is: {correlation_value}"
                            )

    ### Relationship between categorical data between categorical data.
    def cat_to_cat(self, col1, col2):
        if isinstance(col1, str):
            if isinstance(col2, str):
                self.countplot(col1, col2)
                self.contingency_table(col1, col2)
                self.Chi_square(col1, col2)

            elif isinstance(col2, list):
                for value in col2:
                    self.countplot(col1, value)
                    self.contingency_table(col1, value)
                    self.Chi_square(col1, value)
            else:
                print("Enter a sting or a list as parameters for parameter two")
        elif isinstance(col1, list):
            if isinstance(col2, str):
                for value in col1:
                    self.countplot(value, col2)
                    self.contingency_table(value, col2)
                    self.Chi_square(value, col2)

            elif isinstance(col2, list):
                for value in col1:
                    for value2 in col2:
                        
                        self.countplot(value, value2)
                        self.contingency_table(value, value2)
                        self.Chi_square(value, value2)

    # plot the countplot
    def countplot(self, col1, col2):
        sns.countplot(x=col1, hue=col2, data=self.categorical_data)
        plt.title(f"{col1} vs {col2}")
        plt.show()

    # drawing a contingency table
    def contingency_table(self, col1, col2):
        contigency_table = pd.crosstab(
            self.categorical_data[col1], self.categorical_data[col2]
        )
        sns.heatmap(contigency_table, annot=True, cmap="YlGnBu", fmt="d")
        plt.title(f"Contingency table of {col1} vs {col2}")
        plt.show()

    # calculating the chi square value
    def Chi_square(self, col1, col2):
        compare = pd.crosstab(self.categorical_data[col1], self.categorical_data[col2])
        ch12, p, dof, ex = stats.chi2_contingency(compare)
        print(f"Chi_square value {ch12}\np value{p}\ndegree of freedom{dof}")

        if p > 0.05:
            print(f"{col1} is not correlated with {col2}")
        else:
            print(f"{col1} is correlated with {col2} ")

    ### Relationship between continouos data between categorical data.
    def combined_boxplot(self, var1, var2):
        sns.boxplot(x=self.dataframe[var1], y=self.dataframe[var2])
        plt.xlabel(f"{var1}")
        plt.ylabel(f"{var2}")
        plt.title(f"Boxplots of {var1} vs. {var2}")
        plt.show()

    def singleAnova(self, cont_var, cat_var):
        grouped_data = [
            group[cont_var].values for _, group in self.dataframe.groupby(cat_var)
        ]
        f_statistic, p_value = f_oneway(*grouped_data)

        if p_value > 0.05:
            print(f"{cat_var} is not correlated with {cont_var}")
        else:
            print(f"{cat_var} is correlated with {cont_var}")

    def cont_to_cat(self, col1, col2):
        if isinstance(col1, str):  # first input is a string
            if pd.api.types.is_numeric_dtype(
                self.dataframe[col1]
            ):  # when the input is continuous data
                if isinstance(col2, str):  # second is also a string
                    if not pd.api.types.is_numeric_dtype(self.dataframe[col2]):
                        self.combined_boxplot(col2, col1)
                        self.singleAnova(col1, col2)
                    elif pd.api.types.is_numeric_dtype(self.dataframe[col2]):
                        print(f"One of the parameters must be categorical")
                elif isinstance(col2, list):  # second is a list
                    for i, col in enumerate(col2):
                        if not pd.api.types.is_numeric_dtype(self.dataframe[col]):
                            self.combined_boxplot(col, col1)
                            self.singleAnova(col1, col)
                        elif pd.api.types.is_numeric_dtype(self.dataframe[col2]):
                            print(f"One of the parameters must be categorical")
                    plt.tight_layout()
                    plt.show()

            elif not pd.api.types.is_numeric_dtype(
                self.dataframe[col1]
            ):  # when the input is categorical data
                if isinstance(col2, str):
                    if pd.api.types.is_numeric_dtype(self.dataframe[col2]):
                        self.combined_boxplot(col1, col2)
                        self.singleAnova(col2, col1)
                    elif not pd.api.types.is_numeric_dtype(self.dataframe[col2]):
                        print("One of the values must be continuous")

                elif isinstance(col2, list):
                    for i, col in enumerate(col2):
                        if pd.api.types.is_numeric_dtype(self.dataframe[col]):
                            self.combined_boxplot(col1, col)
                            self.singleAnova(col, col1)
                        elif not pd.api.types.is_numeric_dtype(self.dataframe[col2]):
                            print("Öne of the parameters must be continuous")

        elif isinstance(col1, list):
            if isinstance(col2, str):
                if pd.api.types.is_numeric_dtype(self.dataframe[col2]):
                    
                    for i, col in enumerate(col1):
                        if not pd.api.types.is_numeric_dtype(self.dataframe[col]):
                            self.combined_boxplot(col, col2)
                            self.singleAnova(col2, col)

                        else:
                            print("One of the parameters must be categorical")

                elif not pd.api.types.is_numeric_dtype(
                    self.dataframe[col2]
                ):  # for checking
                    
                    for i, col in enumerate(col1):
                       
                        if pd.api.types.is_numeric_dtype(self.dataframe[col]):
                            self.combined_boxplot(col2, col)
                            self.singleAnova(col, col2)

            elif isinstance(col2, list):
                numb_lst2 = len(col2)
                numb_lst1 = len(col1)

                if numb_lst1 == 1 and numb_lst2 == 1:
                    if pd.api.types.is_numeric_dtype(self.dataframe[col1[0]]):
                        if not pd.api.types.is_numeric_dtype(self.dataframe[col2[0]]):
                            plt.figure(figsize=(8, 6))
                            self.combined_boxplot(col2[0], col1[0])
                            self.singleAnova(col1[0], col2[0])
                        else:
                            print("One of parameters must have categorical data")

                    elif not pd.api.types.is_numeric_dtype(self.dataframe[col1[0]]):
                        if pd.api.types.is_numeric_dtype(self.dataframe[col2[0]]):
                            plt.figure(figsize=(8, 6))
                            self.combined_boxplot(col1[0], col2[0])
                            self.singleAnova(col2[0], col1[0])
                        else:
                            print("One of parameters must have continuous data")

                elif numb_lst1 == 1 and numb_lst2 > 1:
                    if pd.api.types.is_numeric_dtype(self.dataframe[col1[0]]):
                        for i, col in enumerate(col2):
                            if not pd.api.types.is_numeric_dtype(self.dataframe[col]):
                                # sns.boxplot(x = self.dataframe[col], y = self.dataframe[col1[0]])
                                self.combined_boxplot(col, col1[0])
                                self.singleAnova(col1[0], col)
                            else:
                                print("One of parameters must have categorical data")

                    elif not pd.api.types.is_numeric_dtype(self.dataframe[col1[0]]):
                        
                        for i, col in enumerate(col2):
                           
                            if pd.api.types.is_numeric_dtype(self.dataframe[col]):
                                self.combined_boxplot(col1[0], col)
                                self.singleAnova(col, col1[0])
                            else:
                                print("One of parameters must have continuous data")

                elif numb_lst1 > 1 and numb_lst2 == 1:
                    
                    if pd.api.types.is_numeric_dtype(self.dataframe[col2[0]]):
                        for i, col in enumerate(col1):
                            if not pd.api.types.is_numeric_dtype(self.dataframe[col]):
                                self.combined_boxplot(col, col2[0])
                                self.singleAnova(col2[0], col)
                            else:
                                print("One of parameters must have categorical data")

                    elif not pd.api.types.is_numeric_dtype(self.dataframe[col2[0]]):
                        for i, col in enumerate(col1):
                            if pd.api.types.is_numeric_dtype(self.dataframe[col]):
                                self.combined_boxplot(col2[0], col)
                                self.singleAnova(col, col2[0])

                            else:
                                print("One of parameters must have continuous data")

                elif numb_lst1 > 1 and numb_lst2 > 1:
                    fig, axes = plt.subplots(numb_lst1, numb_lst2, figsize=(20, 20))
                    for i, x in enumerate(col1):
                        for j, y in enumerate(col2):
                            ax = axes[i, j]
                            if isinstance(col1[i], str):
                                if pd.api.types.is_numeric_dtype(
                                    self.dataframe[x]
                                ) and not pd.api.types.is_numeric_dtype(
                                    self.dataframe[y]
                                ):
                                    sns.boxplot(
                                        x=self.dataframe[y], y=self.dataframe[x], ax=ax
                                    )
                                    ax.set_title(f"Box plot {col1[i]} vs {col2[j]}")
                                    self.singleAnova(x, y)
                                elif not pd.api.types.is_numeric_dtype(
                                    self.dataframe[x]
                                ) and pd.api.types.is_numeric_dtype(self.dataframe[y]):
                                    sns.boxplot(
                                        x=self.dataframe[x], y=self.dataframe[y], ax=ax
                                    )
                                    ax.set_title(f"Box plot {col2[j]} vs {col1[i]}")
                                    self.singleAnova(y, x)
                                else:
                                    print("One of the parameters must be categorical")
                            else:
                                print("Array elements must be strings")

            plt.tight_layout()
            plt.show()
# general function specifically for data cleaning    
    def data_cleaning(self):
        self.remove_missingvalues()
        self.remove_outliers()
        return self.dataframe

