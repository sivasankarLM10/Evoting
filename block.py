import streamlit as st
import hashlib
import datetime
import json
import os


# Define Block class
class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(data_string.encode()).hexdigest()


# Define Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = self.load_chain_from_file()
        if not self.chain:
            self.create_genesis_block()

    def load_chain_from_file(self):
        if not os.path.exists("blockchain_data.json"):
            return []

        with open("blockchain_data.json", "r") as file:
            data = file.read()
            if data:
                return [Block(datetime.datetime.fromisoformat(block_data["timestamp"]), block_data["data"], block_data["previous_hash"]) for block_data in json.loads(data)]
        return []

    def save_chain_to_file(self):
        with open("blockchain_data.json", "w") as file:
            data = json.dumps([block.__dict__ for block in self.chain], default=str)
            file.write(data)

    def create_genesis_block(self):
        genesis_block = Block(datetime.datetime.now(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_hash = self.chain[-1].hash
        new_block = Block(datetime.datetime.now(), data, previous_hash)
        self.chain.append(new_block)
        self.save_chain_to_file()

    def get_latest_block(self):
        return self.chain[-1]

    def get_winner(self):
        candidate_votes = {}
        for block in self.chain[1:]:
            candidate = block.data
            if candidate in candidate_votes:
                candidate_votes[candidate] += 1
            else:
                candidate_votes[candidate] = 1

        if candidate_votes:
            winner = max(candidate_votes, key=candidate_votes.get)
            return winner
        else:
            return "No votes cast yet"


# Initialize the blockchain
blockchain = Blockchain()


# Page for user voting
def user_voting_page():
    st.title("E-Voting System - User Voting Page")
    st.write("Please cast your vote:")

    candidate_options = ["Candidate 1", "Candidate 2", "Candidate 3", "Candidate 4"]
    selected_candidate = st.selectbox("Select Candidate", candidate_options)

    if st.button("Vote"):
        # Add vote to the blockchain
        blockchain.add_block(selected_candidate)
        st.success("Your vote has been recorded successfully!")


# Page for admin to view results
def admin_results_page():
    st.title("E-Voting System - Admin Results Page")
    st.write("Voting Results:")

    winner = blockchain.get_winner()
    st.write("Winner:", winner)

    st.write("Vote Distribution:")
    candidate_votes = {}
    for block in blockchain.chain[1:]:
        candidate = block.data
        if candidate in candidate_votes:
            candidate_votes[candidate] += 1
        else:
            candidate_votes[candidate] = 1

    for candidate, votes in candidate_votes.items():
        st.write(candidate, ": ", votes)


# Main application
def main():
    st.sidebar.title("E-Voting System")
    page = st.sidebar.selectbox("Select Page", ["User Voting", "Admin Results"])

    if page == "User Voting":
        user_voting_page()
    elif page == "Admin Results":
        admin_results_page()


if __name__ == '__main__':
    main()
