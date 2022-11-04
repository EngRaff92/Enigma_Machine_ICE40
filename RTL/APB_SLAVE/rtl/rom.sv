//! ROM: Slave Type
//! 

/** Time Scale */
`timescale 1ns/1ns

module rom#(
    //! Parameters
    parameter ATW           = 5,    //! Length of the address to be used to access the memory (should always be clog2 of DEPTH)
    parameter DEPTH         = 32,   //! Memory Depth (Number of element in the memory)
    parameter DATAW         = 32,   //! Data Length
    parameter ZEROR         = 0,    //! If 0 the the memory will not be initialized with 0, make sure the IMAGE file path is provided (has more priority over IMAGE)
    parameter [800:0] IMAGE = "",   //! IMAGE path from where the BIN/HEX file is located
    parameter ISCLK         = 0     //! If set to 1 the WR and RD process are both clocked otherwise the clock is TIED off to 0
)
(
    //! Ports
    input logic             mem_clk,        //!
    input logic [ATW-1:0]   mem_address,    //!
    input logic             mem_op,         //!
    input logic             mem_cs,         //!
    input logic [DATAW-1:0] mem_wdata,      //!
    output logic [DATAW-1:0]mem_rdata       //!
);

    // Parameter checks
    initial begin: param_check
        /** Parameters cannot be 0 */
        if(ATW == 0)    $error("Address width cannot be 0");
        if(DEPTH == 0)  $error("Memory Depth cannot be 0");
        if(DATAW == 0)  $error("Data width cannot be 0");
        /** ATW should always be clog2 of DEPTH */
        if(ATW != $clog2(DEPTH)) $error("Address width cannot be different from clog2 of DEPTH, ATW: %0d, DEPTH: %0d",ATW, $clog2(DEPTH));
        /** DATAW cannot be greater then 32 */
        if(DATAW > 32) $error("Data width cannot be greater then 32");
        /** we cannot have ZEROR and IMAGE empty */
        assert(~((ZEROR == 0) && (IMAGE == ""))) else $error("ZEROR and IMAGE cannot be both 0, ZEROR: %0d, IMAGE: %0s",ZEROR,IMAGE);
    end

    // Main Memory
    logic [DATAW-1:0] MEMARRAY [DEPTH-1:0];

    // Init Memory
    integer ii;
    initial begin: mem_init
        if(ZEROR) begin: zero_mem
            for(ii=0; ii<DEPTH; ii++) MEMARRAY[ii] = '0;
        end else if(IMAGE != "") begin: mem_image
            $readmemh(IMAGE,MEMARRAY);
            $display("Loading Image file: %0s",IMAGE);
        end else begin
            $display("Image File not Specified: IMAGE: %0s",IMAGE);
        end
    end

    // Generate internal clock based on clock or no_clock
    logic internal_clk; 
    logic clk_en;
    generate
        if(ISCLK)
            assign clk_en = 1;
        else
            assign clk_en = 0;
    endgenerate
    assign internal_clk = mem_clk & clk_en;

    // READ and WRITE process
    generate
        if(ISCLK) begin
            always_ff @(posedge internal_clk) begin: clocking_process
                if(mem_cs) begin
                    if(mem_op == 1) begin
                        MEMARRAY[mem_address]   <= mem_wdata;
                        mem_rdata               <= 0;
                    end else begin
                        mem_rdata               <= MEMARRAY[mem_address];              
                    end
                end
            end
        end else begin
            always_comb begin: no_clock_process
                if(mem_cs) begin
                    if(mem_op == 1) begin
                        MEMARRAY[mem_address]   = mem_wdata;
                        mem_rdata               = 0;
                    end else begin
                        mem_rdata               = MEMARRAY[mem_address];              
                    end
                end
            end            
        end
    endgenerate
endmodule // rom