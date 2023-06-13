'''
Title: MSDS670 Week 5-6 Assignment
Date: 4JUN2021
Author: Jeremy Beard
Purpose: Create visualizations for the DC Political Contributions dataset
Inputs: DC Political Contributions dataset
Outputs: Visualizations
Notes:
    
'''

print('Hello World')

import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dpi = 300

#Set directories
project_dir = r'C:\\Users\\jerem\\OneDrive\\Documents\\School\\_REGIS\\2023-05_Summer\\MSDS670\\MSDS670\\Week5\\'
data_dir = project_dir + r'data\\'
output_dir = project_dir + r'output\\'

#Read csv file into dataframe
df_filename = 'DC political contributions.csv'
df = pd.read_csv(data_dir + df_filename)

#Clean up Amount column
df['Amount'] = df['Amount'].str.replace('$', '')
df['Amount'] = df['Amount'].str.replace(',', '')
df.drop(df[df['Amount'].str.contains('\(')].index, inplace=True)
df['Amount'] = df['Amount'].astype(float)

print('Loaded data')

print(df.head())
print(df.info())

#Grab the data that corresponds with:
# the highest number of state contribution (by sheer count/number)
#   per Contributor Type, and per State
#   only top 10 States


state_counts = df['state'].value_counts(ascending=True)
state_amts = df.groupby('state')['Amount'].sum()
state_amts = state_amts.sort_values(ascending=True)
state_amts = state_amts.tail(10)
candidate_amts = df.groupby('Candidate Name')['Amount'].sum()
candidate_amts = candidate_amts.sort_values(ascending=True)
candidate_amts = candidate_amts.tail(10)
amt_counts = df['Amount'].value_counts(ascending=True)

type_counts = df['Contributor Type'].value_counts(ascending=True)
name_counts = df['Candidate Name'].value_counts(ascending=True)
state_counts = state_counts.tail(10)
top_10_amt_counts = amt_counts.tail(10)
top_10_name_counts = name_counts.tail(10)

print('Candidate AMTS')
print(candidate_amts)
print('STATE_AMTS')
print(state_amts)
print('STATE_COUNTS')
print(state_counts)
print('TYPE_COUNTS')
print(type_counts)
print('TOP_10_AMT_COUNTS')
print(top_10_amt_counts)
print('TOP_10_NAME_COUNTS')
print(top_10_name_counts)

candidateamts = pd.Series(list(candidate_amts.index))
stateamts = pd.Series(list(state_amts.index))
states = pd.Series(list(state_counts.index))
types = pd.Series(list(type_counts.index))
amts = pd.Series(list(top_10_amt_counts.index))
names = pd.Series(list(top_10_name_counts.index))

candidate_amts.index = range(len(candidate_amts))
state_amts.index = range(len(state_amts))
state_counts.index = range(len(state_counts))
type_counts.index = range(len(type_counts))
top_10_amt_counts.index = range(len(top_10_amt_counts))
top_10_name_counts.index = range(len(top_10_name_counts))

# FIGURE 0: Top 10 Total Contribution Amount by State
fig0, ax0 = plt.subplots(figsize=(6,6))
ax0.barh(stateamts, state_amts, color='tab:blue')
ax0.set(xlabel='$ Contributions', ylabel='State', title='Total Contribution Amount by State')
plt.tight_layout()
plot0_filename = 'Total-Contribution-by-State.png'
fig0.savefig(output_dir + plot0_filename, dpi=dpi)

# FIGURE 1: Top 10 Contribution Count by State
fig1, ax1 = plt.subplots(figsize=(6,6))
ax1.barh(states, state_counts, color='tab:orange')
ax1.set(xlabel='# Contributions', ylabel='State', title='Count of Contributions by State')
plt.tight_layout()
plot1_filename = 'Contribution-Count-by-State.png'
fig1.savefig(output_dir + plot1_filename, dpi=dpi)

# FIGURE 2: Contribution Count by Type
fig2, ax2 = plt.subplots(figsize=(6,6))
ax2.barh(types, type_counts, color='tab:green')
ax2.set(xlabel='# Contributions', ylabel='Contribution Type', title='Count of Contributions by Type')
plt.tight_layout()
plot2_filename = 'Contribution-by-Type.png'
fig2.savefig(output_dir + plot2_filename, dpi=dpi)

# FIGURE 3: Contribution Count by Candidate
fig3, ax3 = plt.subplots(figsize=(6,6))
ax3.barh(names, top_10_name_counts, color='tab:red')
ax3.set(xlabel='# Contributions', ylabel='Candidate', title='Count of Contributions by Candidate')
plt.tight_layout()
plot3_filename = 'Contribution-by-Candidate.png'
fig3.savefig(output_dir + plot3_filename, dpi=dpi)

# COMMENTED OUT BECAUSE THIS IS A DUPLICATE CHART
#df_filename2 = 'DC-pivot-01.csv'
#df2 = pd.read_csv(data_dir + df_filename2)
##print(df2.info())
#fig4, ax4 = plt.subplots(figsize=(8,8))
#ax4.barh(df2['State'].tail(10), df2['Sum'].tail(10), width, label='Sum', color='tab:purple')
#ax4.set(xlabel='$ Contributions', ylabel='State', title='Total Contribution Amount by State ($)')
#plt.tight_layout()
#plot4_filename = 'Sum-of-Contributions-by-State.png'
#fig4.savefig(output_dir + plot4_filename, dpi=dpi)

df_filename3 = 'DC-pivot-02.csv'
df3 = pd.read_csv(data_dir + df_filename3)
#print(df3.info())
fig5, ax5 = plt.subplots(figsize=(8,8))
ax5.barh(types, df3['Sum'], label='Sum', color='tab:brown')
ax5.set(xlabel='$ Contributions', ylabel='Type of Contribution', title='Total Contribution Amount by Type ($)')
plt.tight_layout()
plot5_filename = 'Sum-of-Contributions-by-Type.png'
fig5.savefig(output_dir + plot5_filename, dpi=dpi)

df_filename4 = 'DC political contributions sorted.csv'
df4 = pd.read_csv(data_dir + df_filename4)
#Clean up Amount column
df4['Amount'] = df4['Amount'].str.replace('$', '')
df4['Amount'] = df4['Amount'].str.replace(',', '')
df4.drop(df4[df4['Amount'].str.contains('\(')].index, inplace=True)
df4['Amount'] = df4['Amount'].astype(float)
print(df4.info())
fig6, ax6 = plt.subplots(figsize=(8,8))
ax6.barh(df4['Candidate Name'].tail(10), df4['Amount'].tail(10), label='Sum', color='tab:olive')
ax6.set(xlabel='Contribution ($)', ylabel='Candidate', title='Top 10 Individual Contributions by Candidate ($)')
plt.tight_layout()
plot6_filename = 'Individual-Top-10-Contributions-by-Candidate.png'
fig6.savefig(output_dir + plot6_filename, dpi=dpi)

fig7, ax7 = plt.subplots(figsize=(6,6))
ax7.plot(candidate_amts, candidateamts, color='tab:cyan')
ax7.set(xlabel='$ Contributions', ylabel='Candidate', title='Overall Candidate Contributions')
plt.tight_layout()
plot7_filename = 'Overall-Top-10-Contributions-by-Candidate.png'
fig7.savefig(output_dir + plot7_filename, dpi=dpi)

plt.show()
print('Done!')