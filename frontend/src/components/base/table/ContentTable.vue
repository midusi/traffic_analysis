<template>
    <table class="table">
        <thead>
            <tr>
                <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(row, index) in rows" :key="index">
                <td v-for="column in columns" :key="column.key">
                    {{ row[column.key] }}
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    name: "ContentTable",
    props: {
        columns: {},
        rows: {},
    },
};
</script>