from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import json
import os
from docx import Document

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Czheyuan0227%40@localhost:5432/inventory_log'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the LogEntry model
class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    level = db.Column(db.String(50))
    message = db.Column(db.String(500))

    def __repr__(self):
        return f"<LogEntry {self.timestamp} {self.level} {self.message}>"

class GroupLogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    table_data = db.Column(db.Text)  # Store the table data as JSON or CSV string

    def __repr__(self):
        return f"<GroupLogEntry {self.group_name} {self.timestamp}>"


# Define a new model to store saved group data
class GroupData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)
    wip = db.Column(db.Integer)
    fg = db.Column(db.Integer)
    diff = db.Column(db.Integer)

    def __repr__(self):
        return f"<GroupData {self.group_name} {self.timestamp} {self.count} {self.wip} {self.fg} {self.diff}>"

# Initialize the database within the application context
with app.app_context():
    db.create_all()

def log_to_database(level, message):
    with app.app_context():
        log_entry = LogEntry(level=level, message=message)
        db.session.add(log_entry)
        db.session.commit()

def load_and_prepare_data():
    file_path = r"C:\Users\Admin\OneDrive\Desktop\QuickBook\WH01S_8_27.CSV"
    filename = os.path.basename(file_path)
    date_part = filename.replace('.CSV', '').split('_')[-2:]  # Extract the date parts from the filename
    parsed_date = '_'.join(date_part)  # Combine the parts back into a string

    try:
        # Load the CSV file, skipping the first two rows and using no header row
        df = pd.read_csv(file_path, skiprows=3, skipfooter=2,header=None)
        df.columns = ['Part Name', 'Reorder Pt (Min)', 'Max', 'On Hand', 'On Sales Order', 'Available', 'Order', 'On PO', 'Reorder Qty', 'Next Deliv', 'Sales/Week']

        # Filter the columns we're interested in
        df = df[['Part Name', 'On Hand', 'On Sales Order', 'Available']]
        df[['On Hand', 'On Sales Order', 'Available']] = df[['On Hand', 'On Sales Order', 'Available']].apply(pd.to_numeric, errors='coerce').fillna(0)

        groups = {}
        current_group = []
        group_name = None

        for index, row in df.iterrows():
            part_name = row['Part Name']
            all_zeros = (row['On Hand'] == 0 and row['On Sales Order'] == 0 and row['Available'] == 0)

            # Start a new group when encountering a row with all zeros
            if all_zeros:
                if current_group:  # Save the previous group if it exists
                    groups[group_name] = pd.DataFrame(current_group)
                    current_group = []  # Reset the current group

                group_name = part_name  # Update the group name with the new part name

            # Add the row to the current group, this includes 'Total' rows as well
            current_group.append(row.to_dict())

        # After finishing the loop, save the last group if it has not been saved
        if current_group:
            groups[group_name] = pd.DataFrame(current_group)


        log_to_database('INFO', 'Data loaded and processed successfully.')
        return groups, parsed_date  # Return the groups and the date part extracted from the filename
    except Exception as e:
        log_to_database('ERROR', f'Error loading CSV file: {e}')
        return {}, parsed_date  # Return empty in case of an error

groups, parsed_date = load_and_prepare_data()




def get_inventory_totals():
    group_totals = {}
    
    for group_name, df in groups.items():
        if not df.empty:
            # Assume the last row is the total row
            total_row = df.iloc[-1]
            group_totals[group_name] = int(total_row['On Hand'])  # Ensure it's an integer

    return group_totals



@app.route('/')
def index():
    groups_totals = get_inventory_totals()
    return render_template('index.html', groups=groups_totals)



@app.route('/group/<group_name>', methods=['GET', 'POST'])
def group_page(group_name):
    if group_name in groups:
        df = groups[group_name]
        file_path = r"C:\Users\Admin\OneDrive\Desktop\QuickBook\WH01S_8_27.CSV"

        # Extract the filename and parse the date
        filename = os.path.basename(file_path)
        date_part = filename.replace('.CSV', '').split('_')[-2:]  # Extract the last two parts
        parsed_date = '_'.join(date_part)  # Join them back as '7_31'
        
        # Print the parsed date for debugging purposes
        print(f"Parsed Date: {parsed_date}")

        if request.method == 'POST':
            # Process and save the displayed data
            for idx, row in df.iterrows():
                count = int(request.form.get(f'count_{idx}', 0))  # Ensuring value is an integer
                wip = int(request.form.get(f'wip_{idx}', 0))
                fg = int(request.form.get(f'fg_{idx}', 0))
                on_hand = int(row['On Hand'])
                diff = count + wip + fg - on_hand

                # Update DataFrame
                df.at[idx, 'Count'] = count
                df.at[idx, 'WIP'] = wip
                df.at[idx, 'FG'] = fg
                df.at[idx, 'Diff'] = diff

            # Save the table data as a JSON string
            table_data_json = df.to_json(orient='records')
            group_log_entry = GroupLogEntry(group_name=group_name, table_data=table_data_json)
            db.session.add(group_log_entry)
            db.session.commit()
            
            log_to_database('INFO', f'Saved data for group: {group_name}')
            return redirect(url_for('group_page', group_name=group_name))

        # Initialize input fields for display
        for idx, row in df.iterrows():
            df.at[idx, 'Count'] = 0
            df.at[idx, 'WIP'] = 0
            df.at[idx, 'FG'] = 0
            on_hand = int(row['On Hand'])
            df.at[idx, 'Diff'] = 0 - on_hand

        log_to_database('INFO', f'Group page accessed: {group_name}')
        return render_template('group_page.html', group_name=group_name, df=df.to_dict(orient='records'), file_path=parsed_date)
    else:
        log_to_database('WARNING', f'Attempted to access non-existing group: {group_name}')
        return 'Group "{}" not found'.format(group_name), 404



@app.route('/logs/<group_name>')
def view_logs(group_name):
    logs = GroupLogEntry.query.filter_by(group_name=group_name).order_by(GroupLogEntry.timestamp.desc()).all()
    return render_template('logs.html', logs=logs, group_name=group_name)


@app.route('/logs/<group_name>/<int:log_id>')
def log_detail(group_name, log_id):
    log = GroupLogEntry.query.get_or_404(log_id)
    log.table_data = json.loads(log.table_data)  # Convert JSON data to a Python list of dictionaries
    return render_template('log_detail.html', log=log, group_name=group_name)



@app.route('/delete_selected_logs', methods=['POST'])
def delete_selected_logs():
    try:
        selected_logs = request.form.getlist('selected_logs')
        group_name = request.form.get('group_name')  # Get the group name from the form
        if selected_logs:
            for log_id in selected_logs:
                log_entry = GroupLogEntry.query.get(log_id)
                if log_entry:
                    db.session.delete(log_entry)
            db.session.commit()
            log_to_database('INFO', f'Selected logs deleted successfully for group: {group_name}')
        return redirect(url_for('view_logs', group_name=group_name))
    except Exception as e:
        db.session.rollback()
        log_to_database('ERROR', f'Error deleting selected logs: {e}')
        return redirect(url_for('view_logs', group_name=group_name))
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)






































