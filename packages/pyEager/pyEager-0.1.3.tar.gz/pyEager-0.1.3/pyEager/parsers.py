from json import load
import pandas as pd

#### A set of functions to parse the JSON output of nf-core/eager modules into pandas DataFrames ####

def parse_sexdeterrmine_json(json_path, minimal=False):
  """Parses nf-core/eager sex determination results into a pandas DataFrame.

  Args:
      json_path (string): The path to the json file.
      minimal (bool, optional): Should a minimal Data frame be generated?. Defaults to False.

  Returns:
      pandas.DataFrame: A data frame containing the sample-level data from the json file.
        If minimal is True, then only the relative coverages on the X & Y are returned,
        with their respective errors.
  """
  
  with open(json_path) as f:
      data = pd.read_json(f, orient='index')
      data=data.drop(index="Metadata", columns=["tool_name", "version"])
      
      if minimal:
          data=data.drop(columns=['Snps Autosomal', 'XSnps', 'YSnps', 'NR Aut', 'NrX', 'NrY', ])
  
  ## Reset the index
  data.reset_index(inplace=True, names=['id'])
  return data

def parse_damageprofiler_json(json_path):
  """Parses damageprofiler results into a dictionary of pandas DataFrames.

  Args:
      json_path (string): The path to the json file.

  Returns:
      dict: A dictionary containing each part of the json file as its own pandas data frame.
  """
  
  damageprofiler_json_attributes=['metadata', 'lendist_fw', 'dmg_5p', 'summary_stats', 'dmg_3p', 'lendist_rv']
  damage_profiler_results = {}
  
  with open(json_path) as f:
    data=load(f)
    for attr in damageprofiler_json_attributes:
      if attr.startswith('dmg_'):
        damage_profiler_results[attr] = pd.DataFrame(data=data[attr], columns=[attr])
      elif attr.startswith('lendist_'):
        damage_profiler_results[attr] = pd.DataFrame.from_dict(data[attr], orient='index' ,columns=["count"])
        damage_profiler_results[attr].index.name = 'length'
        damage_profiler_results[attr].sort_index(axis=0, ascending=True, inplace=True)
      elif attr == "metadata":
        damage_profiler_results[attr] = pd.DataFrame.from_dict(data[attr], orient='index' ,columns=["value"])
      else:
        damage_profiler_results[attr] = pd.json_normalize(data[attr])
  
  ## Resetting the index cannot be done here, since the output is not a single data frame.
  ## Instead adding the 'id' column happens in compile_damage_table()
  return damage_profiler_results

def parse_nuclear_contamination_json(json_path):
  """Parses nf-core/eager nuclear_contamination results into a pandas DataFrame.

  Args:
      json_path (string): The path to the json file.

  Returns:
      pandas.DataFrame: A data frame containing the library-level nuclear contamination results from the json file.
  """
  
  with open(json_path) as f:
    data=load(f)
    contamination_table=pd.DataFrame.from_dict(data['data'], orient='index' )

  ## Reset the index
  contamination_table.reset_index(inplace=True, names=['id'])
  return contamination_table

def parse_snp_coverage_json(json_path):
  """Parses eigenstratdatabasetools eigenstrat_snp_coverage results into pandas DataFrame.

  Args:
      json_path (string): The path to the json file.

  Returns:
      pandas.DataFrame: A data frame containing the sample-level SNP coverage results from the json file.
  """
  
  with open(json_path) as f:
    data=load(f)
    coverage_table=pd.DataFrame.from_dict(data['data'], orient='index')
  
  ## Reset the index
  coverage_table.reset_index(inplace=True, names=['id'])
  return coverage_table

def parse_endorspy_json(json_path):
  """Parses a single endorspy result JSON into pandas DataFrame.

  Args:
      json_path (string): The path to the json file.

  Returns:
      pandas.DataFrame: A data frame containing the endogenous DNA results from the json file.
  """
  
  with open(json_path) as f:
    data=load(f)
    endogenous_table=pd.DataFrame.from_dict(data['data'], orient='index')
    
    ## Reset the index
    endogenous_table.reset_index(inplace=True, names=['id'])
    return endogenous_table

def parse_eager_tsv(tsv_path):
  """Parse an nf-core/eager input TSV into a pandas DataFrame.

  Args:
      tsv_path (string): The path to the TSV file.

  Returns:
      pandas.DataFrame: A data frame containing the data of the TSV.
  """
  ## TODO Eventually, could add renaming of columns here to keep output consistent between eager 2.* and 3.*
  with open(tsv_path) as f:
    data=pd.read_table(f, sep="\t")
  
  return data

def parse_general_stats_table(general_stats_path):
  """Parse the general_stats_table.txt output of MultiQC into a pandas DataFrame.

  Args:
      general_stats_path (string): The path to the `general_stats_table.txt` TSV file.

  Returns:
      pandas.DataFrame: A data frame containing the data of the TSV.
  """
  with open(general_stats_path) as f:
    data=pd.read_table(f, sep="\t")
  
  return data