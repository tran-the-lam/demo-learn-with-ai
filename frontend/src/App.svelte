<script>
	export let name;
	import { marked } from "marked"; 

	const apiUrl = import.meta.env.VITE_API_URL; // Env variable must start with VITE_
	let startDate = new Date();
    startDate.setDate(startDate.getDate() - 7);
    startDate.setHours(startDate.getHours() + 7);
    startDate = startDate.toISOString().slice(0, 16);

	let endDate = new Date()
	endDate.setHours(endDate.getHours() + 7);
	endDate = endDate.toISOString().slice(0, 16);

	let startEpoch = new Date(startDate).getTime() / 1000;
	let endEpoch = new Date(endDate).getTime() / 1000;
	let emails = "";
	let searchInput = "";
	let data = [];

	const ITEMS_PER_PAGE = 10;
	let currentPage = 1;
	let totalItems = fetchDataCount();

	let selectedConversation = null; 

	function viewDetails(row) {
		selectedConversation = row.chat.messages;
	}

	function closeDetails() {
		selectedConversation = null;
	}

	async function fetchData({ startDate, endDate }) {
		if (emails.length === 0) {
			return [];
		}

		if (startDate.length > 0) {
			startEpoch = new Date(startDate).getTime() / 1000;
		}

		if (endDate.length > 0) {
	        endEpoch = new Date(endDate).getTime() / 1000;
		}

		console.log("Fetch data:", { startDate, endDate, emails, startEpoch, endEpoch });
		let skip = (currentPage - 1) * ITEMS_PER_PAGE;
        const response = await fetch(`${apiUrl}/histories?emails=${emails}&skip=${skip}&limit=${ITEMS_PER_PAGE}&start_time=${Math.floor(startEpoch)}&end_time=${Math.floor(endEpoch)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        return result;
    }

	async function fetchDataCount() {
        const response = await fetch(`${apiUrl}/histories/count?emails=${emails}&start_time=${Math.floor(startEpoch)}&end_time=${Math.floor(endEpoch)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        return result;
	}

	async function searchData() {
		console.log("Search:", { startDate, endDate, searchInput });
		 // Replace newline characters with commas
		emails = searchInput.replace(/\n/g, ',');
		emails = emails.split(',').map(email => email.trim());
		// Call API search data
		data = await fetchData({ startDate, endDate});
		totalItems = await fetchDataCount();
		console.log("Data:", data);
	}

	function clearData() {
		startDate = "";
		endDate = "";
		searchInput = "";
	}

	function formatDate(epochTime) {
        const date = new Date(epochTime * 1000); // Convert epoch time to milliseconds
		const options = {
			timeZone: 'Asia/Bangkok',
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit',
			hour12: false
		};
		return new Intl.DateTimeFormat('en-GB', options).format(date);
    }

	function changePage(newPage) {
        if (newPage > 0 && newPage <= Math.ceil(totalItems / ITEMS_PER_PAGE)) {
            currentPage = newPage;
			fetchData({ startDate, endDate }).then(result => {
                data = result;
            });
        }
    }

</script>

<div class="container">
	<div class="left-panel">
		<h3>Nhập liệu</h3>
		<div class="form-group">
			<label for="start-date">Ngày và giờ bắt đầu:</label>
			<input
				id="start-date"
				type="datetime-local"
				bind:value={startDate}
			/>
		</div>
		<div class="form-group">
			<label for="end-date">Ngày và giờ kết thúc:</label>
			<input id="end-date" type="datetime-local" bind:value={endDate} />
		</div>
		<div class="form-group">
			<label for="search-input">Nhập danh sách email:</label>
			<textarea
				id="search-input"
				bind:value={searchInput}
				rows="6"
				placeholder="Mỗi email trên một dòng."
			></textarea>
		</div>
		<div class="form-group">
			<button on:click={searchData}>Search</button>
			<button on:click={clearData}>Clear</button>
		</div>
	</div>

	<div class="right-panel">
		<h3>Bảng dữ liệu</h3>
		<table class="table">
			<thead>
				<tr>
					<th>Email</th>
					<th>Họ tên</th>
					<th>Mô hình</th>
					<th>Nội dung</th>
					<th>Thời gian</th>
					<th>Số tin nhắn</th>
					<th>Hành động</th>
				</tr>
			</thead>
			<tbody>
				{#each data as row (row.id)}
					<tr>
						<td>{row.email}</td>
						<td>{row.user_name}</td>
						<td>{row.chat.models[0]}</td>
						<td>{row.title}</td>
						<td>{formatDate(row.updated_at)}</td>
						<td>{row.chat.messages.length}</td>
						<td>
							<button on:click={() => viewDetails(row)}>
								<!-- <i class="fas fa-info-circle"></i> -->
								Chi tiết
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	 <div class="pagination">
		<button on:click={() => changePage(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
		<span>Page {currentPage} of {Math.ceil(totalItems / ITEMS_PER_PAGE)}</span>
		<button on:click={() => changePage(currentPage + 1)} disabled={currentPage === Math.ceil(totalItems / ITEMS_PER_PAGE)}>Next</button>
	</div>
</div>

<!-- Conversation Modal -->
{#if selectedConversation}
	{console.log("Selected conversation:", selectedConversation)}  
	<div class="modal">
		<div class="modal-content">
			<button class="close-button" on:click={closeDetails}>Đóng</button>
			<h3>Chi tiết cuộc hội thoại</h3>
			<div class="conversation-container">
				{#each selectedConversation as message (message.id)}
					<div class="message {message.role}">
						<div class="message-content markdown">
							{@html marked(message.content || message.error.content)}
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
{/if}

<style>
	.container {
		display: grid;
		grid-template-columns: 20% 80%;
		height: 100vh;
	}

	.left-panel {
		padding: 20px;
		border-right: 1px solid #ccc;
	}

	.right-panel {
		padding: 20px;
	}

	.form-group {
		margin-bottom: 15px;
	}

	.table {
		width: 100%;
		border-collapse: collapse;
	}

	.table th,
	.table td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: left;
	}

	.pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    .pagination button {
        margin: 0 5px;
        padding: 5px 10px;
    }


	.conversation-container {
		display: flex;
		flex-direction: column;
		gap: 10px;
		padding: 20px;
		background-color: #f9f9f9;
		border: 1px solid #ddd;
		border-radius: 5px;
		max-height: 80vh;
		overflow-y: auto;
	}

	.message {
		display: flex;
		align-items: flex-start;
		gap: 10px;
	}

	.message.user {
		justify-content: flex-end;
	}

	.message.assistant {
		justify-content: flex-start;
	}

	.message-content {
		max-width: 60%;
		padding: 10px;
		border-radius: 5px;
		background-color: #e0f7fa;
		word-wrap: break-word;
	}

	.message.user .message-content {
		background-color: #e8f5e9;
	}

	.markdown {
		white-space: pre-wrap;
	}

	.modal {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.modal-content {
		background: white;
		padding: 20px;
		border-radius: 8px;
		width: 80%;
		max-height: 90%;
		overflow-y: auto;
	}

	.close-button {
		background: red;
		color: white;
		border: none;
		padding: 5px 10px;
		cursor: pointer;
		border-radius: 5px;
		float: right;
	}
</style>
