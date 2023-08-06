import numpy as np
import pandas as pd
import os
import json
from enum import Enum


# Enum for distribution types:
class DistributionType(Enum):
    NORMAL = "normal"
    UNIFORM = "uniform"
    BINOMIAL = "binomial"
    EXPONENTIAL = "exponential"
    MULTINOMIAL = "multinomial"


# Enum for correlation types:
class CorrelationType(Enum):
    LINEAR = "linear"
    QUADRATIC = "quadratic"
    EXPONENTIAL = "exponential"
    POLYNOMIAL = "polynomial"
    CATEGORICAL = "categorical"


# class dataset creator
class DataCreator:
    # Konstruktor
    def __init__(
        self, samples, num_feat, biased, missing_values, outliers, noise, topic
    ):
        self.samples = samples
        self.num_feat = num_feat
        self.biased = biased
        self.missing_values = missing_values
        self.outliers = outliers
        self.noise = noise
        self.topic = topic
        self.all_feature = []

        self.df = pd.DataFrame()

    def generate_Data(self):
        for i in range(self.num_feat):
            print("---------------------------")
            name = self.get_input("What name should this feature have?", str)
            self.name = name
            featType = self.get_input("Is it a categorical or numerical feature?", str)
            self.all_feature.append((name, featType))

            # add a biase
            if self.biased and name.lower() in ["gender", "race"]:
                feature = self.add_bias(name.lower())
                self.df[name] = feature
                continue

            if i == self.num_feat - 1:
                print(
                    "you will now definie your last feature, which should be the target variable"
                )
                feature = self.generate_target_variable()
                continue

            level = self.get_input(
                f"What level does {self.name} have?", int, lambda x: x >= 0
            )
            if level == 0:
                dist_type = self.get_input(
                    f"What type of distribution should {self.name} have?", str
                )
                feature = self.generate_distribution(dist_type)

            elif level >= 1:
                feature = self.generated_correlated_feature()

            self.df[name] = feature

            # add outliers
            if self.outliers and name.lower() != 'target' and featType != 'categorical':
                self.df = self.add_outliers(name, 0.2)

        # adding missing values
        if self.missing_values:
            self.df = self.addmissing_values(0.2)

        # add noise
        if self.noise:
            self.df = self.add_noise(0.1)

        # Write to csv
        self.save_to_csv()

        return self.df

    def generate_distribution(self, dist_type):
        while True:
            try:
                if dist_type == DistributionType.NORMAL.value:
                    mean = self.get_input(
                        "Please type in the center value of the distribution: ", float
                    )
                    sd = self.get_input(
                        "Please type in the standard deviation: ", float
                    )
                    return np.random.normal(loc=mean, scale=sd, size=self.samples)

                elif dist_type == DistributionType.UNIFORM.value:
                    lowB = self.get_input(
                        "Please type in the lower boundary of the distribution: ", float
                    )
                    highB = self.get_input(
                        "Please type in the higher boundary of the distribution: ",
                        float,
                    )
                    return np.random.uniform(low=lowB, high=highB, size=self.samples)

                elif dist_type == DistributionType.BINOMIAL.value:
                    numTrials = self.get_input(
                        "Please type in the number of trials: ", int, lambda x: x >= 0
                    )
                    prob = self.get_input("Please type in the probability: ", float)
                    return np.random.binomial(n=numTrials, p=prob, size=self.samples)

                elif dist_type == DistributionType.EXPONENTIAL.value:
                    s = self.get_input(
                        "Please specify the scale parameter: ", float, lambda x: x >= 0
                    )
                    return np.random.exponential(scale=s, size=self.samples)

                elif dist_type == DistributionType.MULTINOMIAL.value:
                    numCat = self.get_input(
                        "Please type in the number of categories: ",
                        int,
                        lambda x: x >= 0,
                    )
                    probability = self.get_input(
                        "Please set the probabilitie of each different categorie (comma-separated):",
                        str,
                    )

                    start = 0
                    end = numCat
                    cat_array = list(range(start, end))
                    prob_array = json.loads(probability)
                    if len(prob_array) != numCat:
                        raise ValueError(
                            "Number of probabilities must match the number of categories."
                        )

                    # Normalize probabilities to ensure they sum to 1
                    prob_sum = sum(prob_array)
                    prob_array = [p / prob_sum for p in prob_array]
                    return np.random.choice(
                        a=cat_array, size=self.samples, p=prob_array
                    )

                else:
                    print("Invalid distribution name.Please try again.")
                    dist_type = self.get_input(
                        "What type of distribution should the feature have?", str
                    )

            except ValueError as e:
                print(f"Error: {e}")

    def generated_correlated_feature(self):
        numCorr = self.get_input(
            f"How many features does influence {self.name}?", int, lambda x: x >= 0
        )
        arrayFeat = []
        allCoef = []
        feature = np.zeros(self.samples)
        corr_type = self.get_input(
            f"What type of correlation does {self.name} have to the other?", str
        )

        if corr_type == CorrelationType.LINEAR.value:
            for i in range(numCorr):
                while True:
                    help_num = i + 1
                    name_feat = self.get_input(
                        f"Please tell me the name of the {help_num}. influencial feature: ",
                        str,
                    )
                    if name_feat not in self.df.columns:
                        print("Invalid feature name. Available features: ")
                        print(self.df.columns)
                    elif name_feat in arrayFeat:
                        print(
                            "You have already selected this feature. Please choose a different one."
                        )
                    else:
                        break

                corr_coef = self.get_input(
                    f"What is the correlation coefficient with {name_feat}?", float
                )
                arrayFeat.append(name_feat)
                allCoef.append(corr_coef)

            for i in range(numCorr):
                feature = (
                    feature + allCoef[i] * self.df[arrayFeat[i]] + self.df[arrayFeat[i]]
                )

        elif corr_type == CorrelationType.QUADRATIC.value:
            for i in range(numCorr):
                while True:
                    help_num = i + 1
                    name_feat = self.get_input(
                        f"Please tell me the name of the {help_num}. influencial feature: ",
                        str,
                    )
                    if name_feat not in self.df.columns:
                        print("Invalid feature name. Available features: ")
                        print(self.df.columns)
                    elif name_feat in arrayFeat:
                        print(
                            "You have already selected this feature. Please choose a different one."
                        )
                    else:
                        break

                arrayFeat.append(name_feat)

            for i in range(numCorr):
                feature = feature + self.df[arrayFeat[i]] ** 2

        elif corr_type == CorrelationType.EXPONENTIAL.value:
            for i in range(numCorr):
                while True:
                    help_num = i + 1
                    name_feat = self.get_input(
                        f"Please tell me the name of the {help_num}. influencial feature: ",
                        str,
                    )
                    if name_feat not in self.df.columns:
                        print("Invalid feature name. Available features: ")
                        print(self.df.columns)
                    elif name_feat in arrayFeat:
                        print(
                            "You have already selected this feature. Please choose a different one."
                        )
                    else:
                        break
                arrayFeat.append(name_feat)

            for i in range(numCorr):
                feature = np.exp(self.df[arrayFeat[i]] / 2)

        elif corr_type == CorrelationType.CATEGORICAL.value:
            weighted_feature = 0
            num_cat = self.get_input(
                f"How many categories should {self.name} have?", int
            )
            for i in range(numCorr):
                while True:
                    help_num = i + 1
                    name_feat = self.get_input(
                        f"Please tell me the name of the {help_num}. influencial feature: ",
                        str,
                    )
                    if name_feat not in self.df.columns:
                        print("Invalid feature name. Available features: ")
                        print(self.df.columns)
                    elif name_feat in arrayFeat:
                        print(
                            "You have already selected this feature. Please choose a different one."
                        )
                    else:
                        break

                for feat_name, feat_type in self.all_feature:
                    if feat_name == name_feat:
                        help_type = feat_type

                if help_type == "numerical":
                    corr_coef = self.get_input(
                        f"What is the correlation coefficient with {name_feat}?", float
                    )
                    weighted_feature = weighted_feature + corr_coef * self.df[name_feat]

                elif help_type == "categorical":
                    print("drin")
                    first_cat = 0
                    last_cat = self.df[name_feat].max()
                    print(
                        f"You have {last_cat+1} categories for the feature {name_feat}"
                    )
                    print(
                        "To achieve the correct correlation between the feature and target, we need a weighting for each individual category, which should be aggregated. "
                    )
                    qu_weighting = self.get_input(
                        "If the categories already represent a gradation, should this gradation be adopted as the weighting (e.g., 0: low, 1: medium, 2: high). Y/n?",
                        str,
                    )

                    if qu_weighting.lower() == "y":
                        weighted_feature = weighted_feature + self.df[name_feat]
                    elif qu_weighting.lower() == "n":
                        weight = self.get_input(
                            "Please tell me for each influencial categorie what the weight should be (comma-seperated): ",
                            str,
                        )

                        weight_array = json.loads(weight)
                        cat_array = list(range(first_cat, last_cat))
                        combined_list = list(zip(cat_array, weight_array))

                        if len(weight_array) != last_cat + 1:
                            raise ValueError(
                                "Number of probabilities must match the number of categories."
                            )

                        for value_cat, weight_cat in combined_list:
                            weighted_feature = weighted_feature + self.df[
                                name_feat
                            ].map({value_cat: weight_cat}).fillna(0)

            interval_string = self.get_input(
                "Please tell me for the interval for each categorie (comma-seperated): ",
                str,
            )
            interval_list = [
                tuple(map(int, interval.split("-")))
                for interval in interval_string.split(", ")
            ]
            cat_array = list(range(num_cat))
            category_to_interval = {
                category: interval
                for category, interval in zip(cat_array, interval_list)
            }
            feature = pd.Series(0, index=self.df.index)

            for value_cat, interval in category_to_interval.items():
                start, end = interval
                category_mask = (start <= weighted_feature) & (weighted_feature <= end)
                # Assign the current category to the corresponding rows in the feature Series
                feature[category_mask] = value_cat

            print(feature)

        elif corr_type == CorrelationType.EXPONENTIAL.value:
            print("Currently in progress, please select another type")

        else:
            print("Please enter a valid correlation type")

        return feature

    def generate_target_variable(self):
        numCorr = self.get_input(
            "How many features directly influence the target feature?",
            int,
            lambda x: x >= 0,
        )
        weighted_target = 0

        for i in range(numCorr):
            while True:
                help_num = i + 1
                name_feat = self.get_input(
                    f"Please tell me the name of the {help_num}. influencial feature: ",
                    str,
                )
                if name_feat not in self.df.columns:
                    print("Invalid feature name. Available features: ")
                    print(self.df.columns)

                else:
                    break

            for feat_name, feat_type in self.all_feature:
                if feat_name == name_feat:
                    help_type = feat_type

            if help_type == "numerical":
                corr_coef = self.get_input(
                    f"What is the correlation coefficient with {name_feat}?", float
                )
                weighted_target = weighted_target + corr_coef * self.df[name_feat]

            elif help_type == "categorical":
                first_cat = 0
                last_cat = self.df[name_feat].max()
                print(f"You have {last_cat+1} categories for the feature {name_feat}")
                print(
                    "To achieve the correct correlation between the feature and target, we need a weighting for each individual category, which should be aggregated. "
                )
                qu_weighting = self.get_input(
                    "If the categories already represent a gradation, should this gradation be adopted as the weighting (e.g., 0: low, 1: medium, 2: high). Y/n?",
                    str,
                )

                if qu_weighting.lower() == "y":
                    weighted_target = weighted_target + self.df[name_feat]
                elif qu_weighting.lower() == "n":
                    weight = self.get_input(
                        "Please tell me for each categorie what the weight should be (comma-seperated): ",
                        str,
                    )

                    weight_array = json.loads(weight)
                    cat_array = list(range(first_cat, last_cat))
                    combined_list = list(zip(cat_array, weight_array))

                    if len(weight_array) != last_cat + 1:
                        raise ValueError(
                            "Number of probabilities must match the number of categories."
                        )

                    for value_cat, weight_cat in combined_list:
                        weighted_target = weighted_target + self.df[name_feat].apply(
                            lambda x: weight_cat if x == value_cat else 0
                        )

        threshold = self.get_input("Please tell me the decision threshold", float)
        self.df["target"] = weighted_target.apply(lambda x: 1 if x >= threshold else 0)

        return

    def add_noise(self, noise_scale): 
           
        noisy_dataframe = self.df.copy()

        # Generate noise with the same shape as the numerical part of the dataframe
        numerical_features = [
            feat_name
            for feat_name, feat_type in self.all_feature
            if feat_type != "categorical" and feat_name.lower() != "target"
        ]
        noise_shape = (self.df.shape[0], len(numerical_features))
        noise = np.random.normal(loc=0, scale=noise_scale, size=noise_shape)

        # Add noise only to the numerical features
        noisy_dataframe[numerical_features] = self.df[numerical_features] + noise

        return noisy_dataframe

    def add_outliers(self, feature_name, oPercentage):
        min_value = self.df[feature_name].min()
        max_value = self.df[feature_name].max()
        num_outliers = int(len(self.df) * oPercentage)
        outliers = np.random.uniform(low=min_value, high=max_value, size=num_outliers)
        outlier_indices = np.random.choice(
            self.df.index, size=num_outliers, replace=False
        )
        self.df.loc[outlier_indices, feature_name] = outliers

        return self.df

    def addmissing_values(self, missing_percentage):
        for column in self.df.columns:
            if column.lower() == "target":
                continue
            mask = np.random.rand(len(self.df)) < missing_percentage
            self.df.loc[mask, column] = np.nan
        return self.df

    def add_bias(self, feature_type):
        if feature_type == "gender":
            return np.random.choice([0, 1], size=self.samples, p=[0.6, 0.4])

        elif feature_type == "race":
            numCat = int(
                input("How many races do you want to include in your dataset?:  ")
            )
            probabilities = input("Please set the probabilitie of each different race:")

            start = 0
            end = numCat
            cat_array = list(range(start, end))
            prob_array = json.loads(probabilities)

            return np.random.choice(a=cat_array, size=self.samples, p=prob_array)

    def get_input(self, prompt, data_type, validation_func=None):
        while True:
            user_input = input(prompt)
            try:
                user_input = data_type(user_input)
                if validation_func is not None and not validation_func(user_input):
                    print("Invalid input.Please try again.")
                    continue
                return user_input
            except ValueError:
                print("Invalid input. Please try again. ")

    def save_to_csv(self):
        output_folder = "dataset"
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f"generated_dataset_{self.topic}.csv")
        self.df.to_csv(output_file, index=False)
        print(f"Dataset saved to {output_file}")
