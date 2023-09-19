import axios from 'axios';
import {JobPost} from "./schema";

const API_BASE_URL = "http://192.168.1.79:8000";


export const fetchJobPosts = async () => {
    try {
        const response = await axios.get<JobPost[]>(`${API_BASE_URL}/job_post_all/?skip=0&limit=100`);
        return response.data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
}

export const fetchJobPostsFiltered = async () => {
    try {
        const response = await axios.get<JobPost[]>(`${API_BASE_URL}/job_post_filtered/?skip=0&limit=100`);
        return response.data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
}

export const updateJobPost = async (id: number, status: string) => {
    try {
        const response = await axios.post<JobPost>(`${API_BASE_URL}/job_post_update/`, { id, status });
        return response.data;
    } catch (error) {
        console.error("Error updating data:", error);
        throw error;
    }
}