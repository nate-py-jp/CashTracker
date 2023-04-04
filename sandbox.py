import matplotlib.pyplot as plt

# data for the pie chart
pie_data = [{'amount': 500.0, 'category': 'other', 'time': '2023-03-12 20:00:15.580455'},
 {'amount': 300.0,
  'category': 'lunch bentos',
  'time': '2023-03-12 20:01:11.067768'},
 {'amount': 800.0,
  'category': 'weekends',
  'time': '2023-03-12 20:05:04.885751'},
 {'amount': 788.0,
  'category': 'snacks and drinks',
  'time': '2023-03-12 20:48:57.563017'},
 {'amount': 888.0,
  'category': 'weekends',
  'time': '2023-03-13 00:28:38.526384'},
 {'amount': 0.0, 'category': 'other', 'time': '2023-03-13 20:32:06.027352'},
 {'amount': 0.0, 'category': 'other', 'time': '2023-03-23 16:40:40.780670'},
 {'amount': 6789.0, 'category': 'other', 'time': '2023-04-02 16:50:08.122815'}]

# get the non-zero amounts from the pie_data list
amounts = [data['amount'] for data in pie_data if data['amount'] != 0.0]

# data for the total amount
total_data = [{'amount': 0.0, 'time': '2023-03-12 19:59:56.728816'},
 {'amount': 20000.0, 'time': '2023-03-12 20:00:07.213789'},
 {'amount': 0.0, 'time': '2023-03-23 16:40:31.346191'},
 {'amount': 0.0, 'time': '2023-04-02 16:49:49.272440'}]

# calculate the total amount from total_data list
total_amount = sum(data['amount'] for data in total_data if data['amount'] != 0.0)

labels = [data['category'] for data in pie_data if data['amount'] > 0]
amounts.append(total_amount)
labels.append('remaining')

# create the pie chart
plt.pie(amounts, labels=labels, autopct='%1.1f%%', explode=[.1 if label == "remaining" else 0 for label in labels])
plt.title(f"Monthly Cash Deposited: {total_amount:.0f}")
plt.show()







