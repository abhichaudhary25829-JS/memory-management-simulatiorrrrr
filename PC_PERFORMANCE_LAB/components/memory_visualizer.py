import streamlit as st
def render_memory(blocks, total):
    colors={"Free":"#243b53","Allocated":"#10b981","Reserved":"#f59e0b"}
    html="<div class='memory-map'>"
    for b in blocks:
        width=max(5,b["size"]/total*100); status=b["status"]; label=f"{b['block_id']} · {b['size']} KB<br>{status}" + (f"<br>{b['process_name']}" if b.get("process_name") else "")
        html+=f"<div class='memory-block' style='width:{width}%;background:{colors.get(status,"#334155")}'>{label}</div>"
    st.markdown(html+"</div>",unsafe_allow_html=True)
