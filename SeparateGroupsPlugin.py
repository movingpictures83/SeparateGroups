# Objective:
#   To separate "Users" vs "Non-Users" in Mash-Cohort data (metagenomics data)
import pandas as pd
import PyPluMA

class SeparateGroupsPlugin:
    def input(self, infile):
        inputfile = open(infile, 'r')
        self.parameters = dict()
        for line in inputfile:
            contents = line.strip().split('\t')
            self.parameters[contents[0]] = contents[1]

    def run(self):
        pass

    def output(self, outputfile):
       abundance_file = PyPluMA.prefix()+"/"+self.parameters["abundancefile"]
       metadata_file = PyPluMA.prefix()+"/"+self.parameters["metadata"]

       out_users = outputfile+"/"+self.parameters["out1"]
       out_NonUsers = outputfile+"/"+self.parameters["out2"]

       metadata_df = pd.read_csv(metadata_file, sep="\t")
       #metadata_df["group"] = metadata_df["COCAINE USE"].apply(lambda x: 1 if x=="Non-User" else 2)
       metadata_df["group"] = metadata_df[self.parameters["group"]]

       metadata_df["ClientID"] = metadata_df[self.parameters["ClientID"]]
       metadata_df = metadata_df[["group", "ClientID"]]

       df = pd.read_csv(abundance_file, index_col=0)


       df["ClientID"] = df.index
       # transform sample to match metadata
       if (self.parameters["dosplit"] == "True"):
          df["ClientID"] = df["ClientID"].apply(lambda x: x.split("_")[0].replace(".", "/"))

       df = df.merge(metadata_df, how="left", on="ClientID")
       df.index = df["ClientID"]

       df_users = df[df["group"]==self.parameters["group1"]]
       del df_users["group"]
       del df_users["ClientID"]
       df_users.index.names = [""]
       df_users.to_csv(out_users)

       df_non_users = df[df["group"]==self.parameters["group2"]]
       del df_non_users["group"]
       del df_non_users["ClientID"]
       df_non_users.index.names = [""]
       df_non_users.to_csv(out_NonUsers)

       pass
