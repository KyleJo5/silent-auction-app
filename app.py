import streamlit as st
import time
from datetime import datetime

# ============================================
# GAVEL LOGO - ASCII ART
# ============================================
GAVEL_LOGO = """
          ▄▄▄▄▄▄▄▄▄▄▄
         ██▒▒▒▒▒▒▒▒▒▒██
         ██████████████
              ████
              ████
              ████
            ████████
            ██    ██
            ████████
"""

# ============================================
# FUNCTION: Find Highest Bidder
# ============================================
def find_highest_bidder(bidders_dict):
    """
    Find the highest bidder from a dictionary
    Returns: (winner_name, winning_amount)
    """
    if not bidders_dict:
        return None, 0
    
    highest_amount = 0
    winner = ""
    
    for name, amount in bidders_dict.items():
        if amount > highest_amount:
            highest_amount = amount
            winner = name
    
    return winner, highest_amount

# ============================================
# STREAMLIT PAGE CONFIGURATION
# MUST BE THE FIRST STREAMLIT COMMAND!
# ============================================
st.set_page_config(
    page_title="Silent Auction",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================
# INITIALIZE SESSION STATE
# ============================================
if 'bidders' not in st.session_state:
    st.session_state.bidders = {}

if 'auction_started' not in st.session_state:
    st.session_state.auction_started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============================================
# SIDEBAR - LOGO & INFO
# ============================================
with st.sidebar:
    st.title("🎯 Silent Auction")
    st.markdown("---")
    st.code(GAVEL_LOGO, language="text")
    st.markdown("---")
    
    # Auction info
    st.subheader("ℹ️ Auction Info")
    st.write(f"Started: {st.session_state.auction_started}")
    st.write(f"Total Bidders: {len(st.session_state.bidders)}")
    
    # Reset button in sidebar
    if st.button("🔄 Reset Entire Auction", type="secondary", use_container_width=True):
        st.session_state.bidders = {}
        st.session_state.auction_started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success("Auction reset! Starting fresh...")
        time.sleep(1)
        st.rerun()

# ============================================
# MAIN PAGE - HEADER
# ============================================
st.title("🎯 Silent Auction Platform")
st.markdown("---")

# ============================================
# SECTION 1: PLACE A BID
# ============================================
st.header("💰 Place Your Bid")

col1, col2 = st.columns(2)

with col1:
    bidder_name = st.text_input(
        "Your Name:",
        placeholder="Enter your full name",
        help="Enter your name (letters only)"
    )

with col2:
    bid_amount = st.number_input(
        "Bid Amount ($):",
        min_value=0.0,
        step=1.0,
        value=0.0,
        format="%.2f",
        help="Enter your bid amount in dollars"
    )

# Submit bid button
submit_col1, submit_col2 = st.columns([3, 1])
with submit_col1:
    if st.button("🚀 Submit Bid", type="primary", use_container_width=True):
        # Validate input
        if not bidder_name or not bidder_name.strip():
            st.error("❌ Please enter your name!")
        elif not bidder_name.replace(" ", "").replace(".", "").isalpha():
            st.error("❌ Name should contain only letters, spaces, and dots!")
        elif bid_amount <= 0:
            st.error("❌ Bid must be greater than $0!")
        else:
            # Add to bidders
            st.session_state.bidders[bidder_name] = bid_amount
            st.success(f"✅ **{bidder_name}** bid **${bid_amount:,.2f}**")
            
            # Show current highest
            current_winner, current_highest = find_highest_bidder(st.session_state.bidders)
            if current_winner:
                st.info(f"🏆 Current leader: **{current_winner}** with **${current_highest:,.2f}**")
            
            time.sleep(1)
            st.rerun()

with submit_col2:
    if st.button("↻ Clear Form", type="secondary", use_container_width=True):
        st.rerun()

# ============================================
# SECTION 2: CURRENT BIDS
# ============================================
if st.session_state.bidders:
    st.markdown("---")
    st.header("📋 Current Bids")
    
    # Create a nice table
    bid_data = []
    total_value = 0
    
    for name, amount in st.session_state.bidders.items():
        bid_data.append({
            "Bidder": name,
            "Amount": f"${amount:,.2f}",
            "Time": datetime.now().strftime("%H:%M:%S")
        })
        total_value += amount
    
    # Display as columns
    cols = st.columns(3)
    cols[0].metric("Total Bidders", len(st.session_state.bidders))
    cols[1].metric("Total Value", f"${total_value:,.2f}")
    cols[2].metric("Avg Bid", f"${total_value/len(st.session_state.bidders):,.2f}")
    
    # Show all bids in an expandable section
    with st.expander("View All Bids", expanded=True):
        for name, amount in sorted(st.session_state.bidders.items(), key=lambda x: x[1], reverse=True):
            st.write(f"**{name}**: ${amount:,.2f}")

# ============================================
# SECTION 3: DETERMINE WINNER
# ============================================
st.markdown("---")
st.header("🏆 Determine Winner")

winner_col1, winner_col2 = st.columns(2)

with winner_col1:
    if st.button("🎉 Show Winner", type="primary", use_container_width=True):
        if st.session_state.bidders:
            winner, highest_bid = find_highest_bidder(st.session_state.bidders)
            
            # Celebration!
            st.balloons()
            st.success(f"## 🥇 Winner: **{winner}**")
            st.success(f"### 💰 Winning Bid: **${highest_bid:,.2f}**")
            
            # Show ranking
            st.markdown("### 📊 Final Ranking:")
            sorted_bids = sorted(st.session_state.bidders.items(), key=lambda x: x[1], reverse=True)
            
            for i, (name, amount) in enumerate(sorted_bids, 1):
                if i == 1:
                    st.write(f"🥇 **{name}**: ${amount:,.2f} 👑")
                elif i == 2:
                    st.write(f"🥈 {name}: ${amount:,.2f}")
                elif i == 3:
                    st.write(f"🥉 {name}: ${amount:,.2f}")
                else:
                    st.write(f"{i}. {name}: ${amount:,.2f}")
        else:
            st.warning("No bids placed yet! Place a bid first.")

with winner_col2:
    if st.button("📊 View Statistics", type="secondary", use_container_width=True):
        if st.session_state.bidders:
            # Calculate statistics
            bids = list(st.session_state.bidders.values())
            avg_bid = sum(bids) / len(bids)
            max_bid = max(bids)
            min_bid = min(bids)
            
            st.metric("Highest Bid", f"${max_bid:,.2f}")
            st.metric("Lowest Bid", f"${min_bid:,.2f}")
            st.metric("Average Bid", f"${avg_bid:,.2f}")
            st.metric("Total Bidders", len(bids))
        else:
            st.warning("No data to show")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("### 📍 About This Auction")
st.markdown("""
This is a **Silent Auction Platform** built with Streamlit.
- 🔐 **Secure**: All bids are recorded in real-time
- ⚡ **Fast**: Instant winner calculation
- 📱 **Responsive**: Works on mobile and desktop
- 🎯 **Simple**: Easy to use interface
""")

st.caption("Built with ❤️ using Streamlit | Silent Auction Platform v1.0")
