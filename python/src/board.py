from api_object import ApiObject

from pinterest.organic.boards import Board as OrganicBoard

class Board(ApiObject):
    def __init__(self, board_id, api_config, access_token):
        super().__init__(api_config, access_token)
        self.board_id = board_id

    # https://developers.pinterest.com/docs/api/v5/#operation/boards/get
    def get(self):
        if not self.board_id:
            raise ValueError("board_id must be set to get a board")
        """
        return self.request_data(f"/v5/boards/{self.board_id}")
        """
        self.board = OrganicBoard(client=self.access_token.sdk_client, board_id=self.board_id)
        return self.board

    # provides a human-readable identifier for a board
    @classmethod
    def text_id(cls, board_data):
        # simulate Pinterest URL to provide a text identifier
        return (
            "/"
            + cls.field(board_data, "owner")["username"]
            + "/"
            + cls.field(board_data, "name").lower().replace(" ", "-")
            + "/"
        )

    @classmethod
    def print_summary(cls, board_data):
        print("--- Board Summary ---")
        print(f"Board ID: {cls.field(board_data, 'id')}")
        print(f"Name: {cls.field(board_data,'name')}")
        print(f"Description: {cls.field(board_data, 'description')}")
        print(f"Privacy: {cls.field(board_data, 'privacy')}")
        print("--------------------")

    # https://developers.pinterest.com/docs/api/v5/#operation/boards/create
    def create(self, board_data):
        """
        OPTIONAL_ATTRIBUTES = ["description", "privacy"]
        create_data = {
            "name": board_data["name"],
        }
        for key in OPTIONAL_ATTRIBUTES:
            value = board_data.get(key)
            if value:
                create_data[key] = value

        board_data = self.post_data("/v5/boards", create_data)
        """
        board = OrganicBoard.create(
            name=self.field(board_data, "name"),
            description=self.field(board_data, "description"),
            privacy=self.field(board_data, "privacy"),
            client=self.access_token.sdk_client
        )
        self.board = board
        self.board_id = board.id
        return board

    # https://developers.pinterest.com/docs/api/v5/#operation/boards/delete
    def delete(self):
        """
        self.delete_and_check(f"/v5/boards/{self.board_id}")
        """
        OrganicBoard.delete(client=self.access_token.sdk_client, board_id=self.board_id)

    # https://developers.pinterest.com/docs/api/v5/#operation/boards/list_pins
    def get_pins(self, query_parameters=None):
        """
        return self.get_iterator(f"/v5/boards/{self.board_id}/pins", query_parameters)
        """
        return self.get_sdk_iterator(self.board.list_pins, query_parameters)

    # https://developers.pinterest.com/docs/api/v5/#operation/board_sections/list
    def get_sections(self, query_parameters=None):
        """
        return self.get_iterator(
            f"/v5/boards/{self.board_id}/sections", query_parameters
        )
        """
        return self.get_sdk_iterator(self.board.list_sections, query_parameters)

    @classmethod
    def print_section(cls, section_data):
        print("--- Board Section ---")
        print(f"Section ID: {cls.field(section_data, 'id')}")
        print(f"Name: {cls.field(section_data, 'name')}")
        print("---------------------")

    # https://developers.pinterest.com/docs/api/v5/#operation/board_sections/create
    def create_section(self, section_data):
        create_data = {
            "name": section_data["name"],
        }
        return self.post_data(f"/v5/boards/{self.board_id}/sections", create_data)

    # https://developers.pinterest.com/docs/api/v5/#operation/board_sections/list_pins
    def get_section_pins(self, section_id, query_parameters=None):
        """
        return self.get_iterator(
            f"/v5/boards/{self.board_id}/sections/{section_id}/pins", query_parameters
        )
        """
        qp = dict(query_parameters or {})
        qp['section_id'] = qp
        return self.get_sdk_iterator(self.board.list_pins, query_parameters)
